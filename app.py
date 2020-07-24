from flask import Flask, render_template, request, abort, session, flash, redirect, jsonify
import sql
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "hazala"

config = open("config.json", "r")
config = json.load(config)


@app.route("/")
def home():
    return render_template("index.html", posts=sql.readAllPostsWithLimit(config["posts"]),year = datetime.now().year,tittle = 'Bloggir')



@app.route("/post")
def post():
    return render_template("post.html", posts=sql.readAllPosts(), le = len(sql.readAllPosts()),year = datetime.now().year,tittle = 'All Posts in Bloggir')


@app.route("/post/<slug>")
def postview(slug):
    if slug in sql.slugs():
        return render_template("postview.html", post=sql.readPostBySlug(slug),year = datetime.now().year,tittle = sql.readPostBySlug(slug)["tittle"])
    else:
        abort(404)


@app.route("/edit/new-post")
def newpost():
    return render_template

@app.route("/cp")
def cp():
    if "login" in session:
        return render_template("cp.html", posts=sql.readAllPostsByAuthor(session["login"]),year = datetime.now().year,tittle = 'Control Pannel')
    else:
        return redirect("/cplogin")


@app.route("/cplogin", methods=["GET", "POST"])
def cplogin():
    if request.method == 'POST':
        uname = str(request.form.get("uname"))
        password = str(request.form.get("pass"))
        if sql.authenticateuser(uname, password):
            session["login"] = uname
            return redirect("/cp")
    return render_template("cplogin.html",tittle = 'Login to Bloggir')


@app.route("/update/<slug>", methods=["POST"])
def update(slug):
    if session["login"] == sql.getAuthorUserName(slug):
        if request.method == "POST":
            rdata = request.get_json()
            sql.updatePost(tittle=rdata["tittle"], tagline=rdata['tagline'],
                           content=rdata['content'], slug=slug, date=date.today())
            print(rdata)
            return jsonify("sucess")
    else:
        return redirect("/cplogin")


@app.route("/edit/<slug>")
def editpost(slug):
    if session["login"] == sql.getAuthorUserName(slug):
        return render_template("edit.html", post=sql.readPostBySlug(slug),tittle = f"Edit {sql.readPostBySlug(slug)['tittle']}")
    else:
        return redirect("/cplogin")


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
                return render_template('signup.html',tittle = 'SignUp for Bloggir')
            sql.signUpUser(name,email,uname, password)
            return redirect("/cplogin")
        else:
            flash("User exists")
            return render_template("signup.html")
        
    return render_template("signup.html",tittle = 'SignUp for Bloggir')

if __name__ == '__main__':
    app.run(debug=True)
