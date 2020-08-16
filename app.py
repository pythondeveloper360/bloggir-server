from flask import Flask, render_template, request, abort, session, flash, redirect, jsonify,url_for,Markup
import sql
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "hazala"

config = open("config.json", "r")
config = json.load(config)


@app.route("/")
def home():
    return render_template("index.html", posts=sql.readAllPosts(), year=datetime.now().year, tittle='Bloggir')


@app.route("/post")
def post():
    return render_template("post.html", posts=sql.readAllPosts(), le=len(sql.readAllPosts()), year=datetime.now().year, tittle='All Posts in Bloggir')


@app.route("/post/<slug>")
def postview(slug):
    if slug in sql.slugs():
        return render_template("postview.html", post=sql.readPostBySlug(slug),content = Markup(sql.readPostBySlug(slug)['content']), year=datetime.now().year, tittle=sql.readPostBySlug(slug)["tittle"])
    else:
        abort(404)


@app.route("/newpost", methods=['GET','POST'])
def new_post():
    if 'login' in session:
        if request.method == 'POST':
            data = request.get_json()
            name = sql.getNameFromUserName(session['login'])
            sql.insertPost(data['tittle'], data['tagline'], data['content'], data['slug'],
                        date=f'{datetime.now().day} - {datetime.now().month} - {datetime.now().year}', author=name, authorusername=session['login'])
            return redirect('cp')
        else:
            return render_template('newpost.html')
    else:
        return redirect("/cplogin?redirect=newpost")


@app.route("/cp",methods = ['GET'])
def cp():
    if "login" in session:
        if request.args:
            redirect_url = request.args.get('redirect')
            print(request.args)
            return redirect(f"/{redirect_url}")
        return render_template("cp.html", posts=sql.readAllPostsByAuthor(session["login"]), year=datetime.now().year, tittle='Control Pannel',user = session['login'])
    else:
        return redirect("/cplogin")

# @app.route("/login",methods = ["POST"])
# def login():
#     data = request.get_json()
#     if sql.authenticateuser(data['uname'],data['password']):
#         return True

redirect_url = ''
@app.route("/cplogin", methods=["GET", "POST"])
def cplogin():
    global redirect_url
    if request.args:
        print(request.args.get("redirect"))
        redirect_url = "/"+request.args.get('redirect')

    if request.method =='POST':
        uname = request.form.get('uname')
        password = request.form.get('pass')
        if sql.authenticateuser(uname,password):
            session['login'] = uname
        else:
            flash("Username or password doesn't match")
            return render_template('cplogin.html')
    if 'login' in session and redirect_url:
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
        return redirect(url_for("cplogin",redirect = f'/edit/{slug}'))


@app.route("/delete/<slug>", methods=["POST"])
def delete(slug):
    if session["login"] == sql.getAuthorUserName(slug):
        sql.deletePost(slug)
        return redirect("/cp")
    else:
        abort(400)
    return redirect("/cplogin")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get('name')
        uname = request.form.get('uname')
        email = request.form.get('email')
        password = request.form.get('pass')
        if (sql.checkuser(email)) == False:
            if len(password) < 10:
                flash("Password must be longer than 10 characters")
                return render_template('signup.html', tittle='SignUp for Bloggir')
            sql.signUpUser(name, email, uname, password)
            return redirect("/cplogin")
        else:
            flash("User exists")
            return render_template("signup.html")

    return render_template("signup.html", tittle='SignUp for Bloggir')


if __name__ == '__main__':
    app.run(debug = True)
