from flask import Flask, render_template, request, abort, session, flash, redirect, jsonify, url_for, Markup, jsonify, Response,make_response
import sql
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "hazala"

config = open("config.json", "r")
config = json.load(config)


@app.route("/")
def home():
    if "login" in session:
        return render_template("sindex.html", posts=sql.readAllPosts()[::-1], year=datetime.now().year, tittle='Bloggir')
    return render_template("index.html", posts=sql.readAllPosts()[::-1], year=datetime.now().year, tittle='Bloggir')


@app.route("/post")
def post():
    return render_template("post.html", posts=sql.readAllPosts()[::-1], le=len(sql.readAllPosts()), year=datetime.now().year, tittle='All Posts in Bloggir')


@app.route("/post/<slug>")
def postview(slug):
    if slug in sql.slugs():
        return render_template("postview.html", post=sql.readPostBySlug(slug), content=Markup(sql.readPostBySlug(slug)['content']), year=datetime.now().year, tittle=sql.readPostBySlug(slug)["tittle"])
    else:
        abort(404)


@app.route('/mypost')
def mypost():
    if 'login' in session:
        le = len(sql.readAllPostsByAuthor(session['login']))
        le = le if le else "No post yet"
        return render_template("post.html", posts=sql.readAllPostsByAuthor(session['login'])[::-1], le=le, year=datetime.now().year, tittle="All Posts by {}".format(sql.getNameFromUserName(session['login'])))

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
            name = sql.getNameFromUserName(session['login'])
            sql.insertPost(tittle, tagline, content, slug,
                           date=f'{datetime.now().day} - {datetime.now().month} - {datetime.now().year}', author=name, authorusername=session['login'])
            return redirect('/cp')
        else:
            return render_template('newpost.html')
    else:
        return redirect("/cplogin?redirect=newpost")


@app.route("/cp", methods=['GET'])
def cp():
    if "login" in session:
        return render_template("cp.html", posts=sql.readAllPostsByAuthor(session["login"]), year=datetime.now().year, tittle='Control Pannel', user=session['login'])
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
            flash("Username or password does not nbsp match")
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


@app.route("/edit/<slug>")
def editpost(slug):
    if 'login' in session:
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
        name = request.form.get('name')
        username = request.form.get('uname')
        email = request.form.get('email')
        password = request.form.get('pass')
        work = sql.signUpUser(name, email, username, password)
        if work:
            return redirect("/cplogin")
        else:
            flash("Username exists")
            return redirect("/signup")

    return render_template("signup.html", tittle='SignUp for Bloggir')


@app.route("/pouch")
def pouch():
    if request.method == "POST": 
        if "login" in session:
            return render_template('pouch.html', data=sql.informationByusername(session['login']))
        return redirect("/cplogin?redirect=pouch")
    elif


@app.route("/changepassword", methods=["POST"])
def changepassword():
    if "login" in session:
        data = request.get_json()
        work = sql.changePassword(session['login'],data['current'],data['newpassword'])
        if work:
            return jsonify({"done":"sdfsd"})
        else:
            return jsonify({"not done":"dsd"})
    else:
        return make_response("eroor")
@app.route('/logout')
def logout():
    if 'login' in session:
        session.clear()
        return redirect('/')
    else:
        return redirect('/cplogin?redirect=cp')


if __name__ == '__main__':
    app.run(debug=True)
