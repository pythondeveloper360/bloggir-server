import json
from datetime import datetime
from threading import Thread

from flask import (Flask, Markup, Response, abort, flash, jsonify,
                   make_response, redirect, render_template, request, session,
                   url_for)

import sql

app = Flask(__name__)
app.secret_key = "hazala"
# TODO need to create  route to read comment of specic post or all comments to author


@app.after_request
def after_request_func(response):
    origin = request.headers.get('Origin')
    if request.method == 'OPTIONS':
        # TODO i think I need to add content-type header in access-control-allow-headers on post requests
        response = make_response()

        response.headers.add("Access-Control-Allow-Origin", origin)
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-type, username,password,token,client_id,device_name')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, OPTIONS, PUT, PATCH, DELETE')
    else:
        pass

    return response


@app.route("/")
def home():
    if "login" in session:
        return render_template("index.html", base="baseadmin", posts=sql.readAllPosts()[::-1], year=datetime.now().year, page_tittle='Bloggir')
    return render_template("index.html", base="base", posts=sql.readAllPosts()[::-1], year=datetime.now().year, page_tittle='Bloggir')


@app.route("/allposts")
def post():
    if 'login' in session:
        return render_template("post.html", posts=sql.readAllPosts()[::-1], base='baseadmin', le=len(sql.readAllPosts()), year=datetime.now().year, page_tittle='All Posts in Bloggir')
    return render_template("post.html", posts=sql.readAllPosts()[::-1], base='base', le=len(sql.readAllPosts()), year=datetime.now().year, page_tittle='All Posts in Bloggir')


@app.route("/post/<slug>")
def postview(slug):
    if "login" in session:
        if session["login"] != sql.getAuthorUserName(slug):
            sql.postview(slug)
        if slug in sql.slugs():
            return render_template("postview.html", url=f'post/{slug}', base="baseadmin", login_user=session['login'], like=sql.check_liked_by_user(session['login'], slug), post=sql.readPostBySlug(slug), login=True, content=Markup(sql.readPostBySlug(slug)['content']), year=datetime.now().year, page_tittle=sql.readPostBySlug(slug)["tittle"], comments=sql.getComment(slug).repr())
        else:
            abort(404)
    else:
        if slug in sql.slugs():

            return render_template("postview.html", url=f'post/{slug}', base="base", post=sql.readPostBySlug(slug), content=Markup(sql.readPostBySlug(slug)['content']), year=datetime.now().year, login=False, page_tittle=sql.readPostBySlug(slug)["tittle"], comments=sql.getComment(slug).repr())
        else:
            abort(404)


@app.route('/mypost')
def mypost():
    if 'login' in session:
        le = len(sql.readAllPostsByAuthor(session['login']))
        le = le if le else "No post yet"
        return render_template("post.html", base="baseadmin", posts=sql.readAllPostsByAuthor(session['login'])[::-1], le=le, year=datetime.now().year, page_tittle="All Posts by {}".format(sql.getNameFromUserName(session['login'])))

    else:
        return redirect('/cplogin?redirect=mypost')


@app.route("/newpost", methods=['GET', 'POST'])
def new_post():
    if 'login' in session:
        if request.method == 'POST':
            tittle = request.form.get('tittle')
            slug = request.form.get('slug')
            tagline = request.form.get('tagline')
            content = request.form.get('content')
            Thread(target=sql.insertPost, args=(tittle, tagline, content, slug,
                                                session['login'])).start()
            return redirect('/cp')
        else:
            return render_template('newpost.html')
    else:
        return redirect("/cplogin?redirect=newpost")


@app.route("/cp", methods=['GET'])
def cp():
    if "login" in session:
        return render_template("cp.html", posts=sql.readAllPostsByAuthor(session["login"]), year=datetime.now().year, tittle='Control Pannel', page_tittle='Control Pannel', user=session['login'])
    else:
        return redirect("/cplogin?redirect=cp")


redirect_url = ''


@app.route("/cplogin", methods=["GET", "POST"])
def cplogin():
    global redirect_url
    if request.args:
        redirect_url = "/"+request.args.get('redirect')

    if request.method == 'POST':
        uname = request.form.get('uname')
        password = request.form.get('pass')
        if sql.authenticateuser(uname, password):
            session['login'] = uname
        else:
            flash("Username or password does not match")
            return render_template('cplogin.html')
    if 'login' in session and redirect_url != '':
        if r'%2F' in redirect_url:
            redirect_url = redirect_url.replace(r'%2F', "/")
        return redirect(redirect_url)
    elif redirect_url == '':
        redirect_url = '/cp'
        return redirect(redirect_url)
    else:
        return render_template("cplogin.html")


@app.route("/update/<slug>", methods=["POST"])
def update(slug):
    if "login" in session:
        if request.method == "POST":
            rdata = request.get_json()
            sql.updatePost(tittle=rdata["tittle"], tagline=rdata['tagline'],
                           content=str(rdata['content']), slug=slug, date=f'{datetime.now().day} - {datetime.now().month} - {datetime.now().year}')

            return jsonify("sucess")
    else:
        return redirect("/cplogin")


@app.route("/edit/<slug>", methods=["POST", "GET"])
def editpost(slug):
    if 'login' in session:
        if request.method == "POST":
            tittle = request.form.get('tittle')
            tagline = request.form.get('tagline')
            content = request.form.get('content')
            sql.updatePost(tittle, tagline, content, slug,
                           date=f'{datetime.now().day} - {datetime.now().month} - {datetime.now().year}')
            return redirect('/cp')
        return render_template("edit.html", post=sql.readPostBySlug(slug), tittle=f"Edit {sql.readPostBySlug(slug)['tittle']}")
    else:
        return redirect(f"/cplogin?redirect=edit/{slug}")


@app.route("/delete/<slug>", methods=["POST"])
def delete(slug):
    if 'login' in session:
        sql.deletePost(slug)
        return jsonify({"succes": "true"})
    else:
        abort(400)
        return jsonify({"succes": "false"})


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        work = sql.signUpUser(request.form.get('name'), request.form.get(
            'email'), request.form.get('uname'), request.form.get('pass'), request.form.get('about'))
        if work:
            session["login"] = request.form.get('uname')
            return redirect('/')
        else:
            flash("Username is already taken")
            return render_template("signup.html", tittle='SignUp for Bloggir')

    return render_template("signup.html", tittle='SignUp for Bloggir')


@app.route("/setting")
def setting():
    if request.method == "GET":
        if "login" in session:
            return render_template('setting.html', data=sql.informationByusername(session['login']))
        return redirect("/cplogin?redirect=setting")
    if request.method == "POST":
        if "login" in session:
            data = request.get_json()
            sql.editprofile(session["login"], data['name'], data['about'])
            return jsonify("Done")


@app.route("/changepassword", methods=["POST"])
def changepassword():
    if "login" in session:
        data = request.get_json()
        work = sql.changePassword(
            session['login'], data['current'], data['newpassword'])
        if work:
            return make_response("Done", 200)
        else:
            return make_response("Not done", 401)
    else:
        return make_response("eroor")


@app.route('/logout')
def logout():
    if 'login' in session:
        session.clear()
        return redirect('/')
    else:
        return redirect('/cplogin?redirect=cp')


@app.route("/like/<slug>", methods=["POST"])
def like(slug):
    if "login" in session:
        if slug != "":
            if (sql.like_blog(session['login'], slug)):
                return{"work": "done"}
            else:
                return {'work': 'not done'}

    else:
        return jsonify({"work": "not_done"})


@app.route("/unlike/<slug>", methods=["POST"])
def unlike(slug):
    if "login" in session:
        if slug != "":
            if (sql.unlike_blog(session['login'], slug)):
                return{"work": "done"}
            else:
                return {"work": "not done"}
        else:
            return jsonify({'wrok': 'not done'})
    else:
        return jsonify({"work": "not_done"})


@app.route('/comment/<slug>', methods=['POST'])
# TODO need to add threadig in this route
def comment_create(slug):
    data = request.get_json()
    Thread(target=sql.add_comment, args=(
        slug, session['login'], data['comment'], data['date'])).start()
    return jsonify({"word": ""})


@app.route('/readcomments/<slug>')
def readComments(slug):
    if "login" in session:
        return render_template('comments.html', comments=sql.getComment(slug))
    else:
        return abort(400)

# @Api Portion


@app.route('/api/posts', methods=["POST"])
def api_post():
    d = request.get_json()
    if d.get('by'):
        response = jsonify({"posts": sql.readAllPostsByAuthor(authorusername=d['by'])})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        response = jsonify({"posts": sql.readAllPosts()})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response



@app.route("/api/loginAuth", methods=["POST"])
def api_loginAuth():

    hData = request.headers
    work = sql.authenticateLogin(username=hData.get(
        'username'), cleint_id=hData.get('client_id'), token=hData.get('token'))

    if work:
        response = jsonify({"status": "done"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:

        response = jsonify({"status": "unathourized"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


@app.route('/api/login', methods=['POST'])
def api_login():
    hData = request.headers
    w = sql.login(
        username=hData.get('username'), password=hData.get('password'), device_name=hData.get('device_name'))
    if w:
        response = jsonify(w)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        response = jsonify({"status": "unauthorized"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


@app.route('/api/logout', methods=['POST'])
def api_logout():
    hData = request.headers
    work = sql.logout(username=hData.get('username'),
                      client_id=hData.get('client_id'))
    if work:
        response = jsonify({'status': "done"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


@app.route('/api/postBySlug', methods=["POST"])
def api_post_by_slug():
    jData = request.get_json()
    if jData.get('slug'):
        work = sql.readPostBySlug(jData.get('slug'))
        if work:
            response = jsonify({"status": "done", "post": work})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        else:
            print('second else')
            response = jsonify({'status': 'not done'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    else:
        print('last else')
        response = jsonify({'status': 'not done'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


@app.route('/api/newPost', methods=["POST"])
def api_newPost():
    jData = request.get_json()
    hData = request.headers
    if (sql.authenticateLogin(username=hData.get(
            'username'), cleint_id=hData.get('client_id'), token=hData.get('token'))):
        work = sql.insertPost(tittle=jData.get('tittle'), content=jData.get('content'), slug=jData.get(
            'slug'), tagline=jData.get('tagline'), authorusername=jData.get('authorusername'))
        response = jsonify({"status": True} if work else {"status": False})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        response = jsonify({"status": 'Falsey'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
@app.route('/api/getComments')
def api_get_comments():
    args = request.args
    if args.get('slug'):
        work = list(sql.getComment(args.get('slug')))
        response = jsonify({"comments":work})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        response = jsonify({"status": False})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

if __name__ == '__main__':
    app.run(debug=True)
