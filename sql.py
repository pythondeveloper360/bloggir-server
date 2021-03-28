import psycopg2
from psycopg2 import sql
import json
import os
import utils

db = psycopg2.connect(
    user='xubuuanpszwwcx',
    password='3e2b69885d81e646182281d1cfb60ed02a6a584d24b62ba81f4734f1ed8c5e2c',
    host='ec2-54-197-254-117.compute-1.amazonaws.com',
    port='5432',
    database='dffngl3u0qkkld'
)
# db = psycopg2.connect(user = "hanzala",
#                       password = 'qsa-1299',
#                       host = "localhost",
#                       port = '5432',
#                       database = 'mydb'  )
cursor = db.cursor()

"""
    |Post|

    Id
    Tittle
    Tagline
    Content
    Slug
    Date created/updated
    author : name
    author : username

id,tittle,tagline,content,slug,date,author,authorusername
"""
"""

    |Users|
    Id
    Name
    Email
    Username
    Password

"""


def readAllPosts():
    array = []
    sqlquery = sql.SQL('SELECT id,tittle,tagline,slug,date,author FROM post')
    cursor.execute(sqlquery)
    data = cursor.fetchall()
    # print(data)
    for i in range(len(data)):
        array.append(dict(id=data[i][0], tittle=data[i][1], tagline=data[i][2], slug=data[i][3], date=data[i][4], author=data[i][5]))
    return array


def insertPost(tittle, tagline, content, slug, date, author, authorusername,image):
    try:
        sqlquery = sql.SQL('INSERT INTO post ({tittle},{tagline},{content},{slug},{date},{author},{authorusername},{likes},{view},{image}) values (%s,%s,%s,%s,%s,%s,%s,0,1,%s);').format(
            tittle=sql.Identifier("tittle"), tagline=sql.Identifier("tagline"),
            content=sql.Identifier("content"),
            slug=sql.Identifier("slug"), date=sql.Identifier("date"),
            author=sql.Identifier("author"),
            authorusername=sql.Identifier("authorusername"),
            likes = sql.Identifier("likes"),view = sql.Identifier("view"),
            image = sql.Identifier("image"))


        cursor.execute(sqlquery, (tittle, tagline, content,
                                slug, date, author, authorusername,image))
        db.commit()
        return True
    except:
        pass


def readPostBySlug(slug):
    sqlquery = sql.SQL('SELECT id,tittle,tagline,content,slug,date,author,authorusername,view,likes FROM post where {slug} = %s;').format(slug=sql.Identifier("slug"))
    cursor.execute(sqlquery, (slug,))
    data = cursor.fetchone()
    return dict(id=data[0], tittle=data[1], tagline=data[2], content=data[3],
                slug=data[4], date=data[5], author=data[6], authorusername=data[7],
                view = data[8],likes = data[9])


def slugs():
    array = []
    sqlquery = sql.SQL('SELECT {slug} from post;').format(
        slug=sql.Identifier("slug"))
    cursor.execute(sqlquery)
    data = cursor.fetchall()
    for i in range(len(data)):
        array.append(data[i][0])
    return array


def readAllPostsByAuthor(authorusername):
    array = []
    sqlquery = sql.SQL('SELECT id,tittle,tagline,slug,date,author,authorusername FROM post where {authorusername} = %s').format(
        authorusername=sql.Identifier("authorusername"))
    cursor.execute(sqlquery, (authorusername,))
    data = cursor.fetchall()
    for i in range(len(data)):
        array.append(dict(id=data[i][0], tittle=data[i][1], tagline=data[i][2], slug=data[i][3], date=data[i][4], author=data[i][5], authorusername=data[i][6]))
    return array

def postview(slug):
    if slug in slugs():
        sqlquery = sql.SQL('select view from post where {slug} = %s').format(
            slug = sql.Identifier("slug")
            )
        cursor.execute(sqlquery,(slug,))
        data = cursor.fetchone()[0]
        view = data if data else 0
        sq = sql.SQL('update post set view = %s where {slug} = %s').format(
            slug = sql.Identifier("slug")
        )
        cursor.execute(sq,((int(view)+1),slug))
        db.commit()
        return True
    else:
        return False

def informationByusername(username):
    re = {}
    sqlquery = sql.SQL('select * from users where {username} = %s').format(
        username=sql.Identifier("username")
    )
    cursor.execute(sqlquery, (username,))
    data = cursor.fetchone()
    re = {"name": data[0], "email": data[1],
        "username": data[2],"about":data[4]} if data else False
    return re


def getAuthorUserName(slug):
    sqlquery = sql.SQL('SELECT authorusername from post where {slug} = %s;').format(
        slug=sql.Identifier("slug"))
    cursor.execute(sqlquery, (slug,))
    data = cursor.fetchone()
    return data[0] if data else "no user"


def getNameFromUserName(username):
    sqlquery = sql.SQL('select {name} from "users" where {username} = %s;').format(
        name=sql.Identifier("name"), username=sql.Identifier("username"))
    cursor.execute(sqlquery, (username,))
    data = cursor.fetchone()
    if data:
        return data[0]
    else:
        return False


def deletePost(slug):
    sqlquery = sql.SQL('DELETE FROM post WHERE {slug} = %s;').format(
        slug=sql.Identifier("slug"))
    cursor.execute(sqlquery, (slug,))
    db.commit()


def updatePost(tittle, tagline, content, slug, date):
    sqlquery = sql.SQL('UPDATE post set {tittle} = %s, {tagline} = %s, {content} = %s, {date} = %s WHERE {slug} = %s;').format(
        tittle=sql.Identifier("tittle"), tagline=sql.Identifier("tagline"), content=sql.Identifier("content"), date=sql.Identifier("date"), slug=sql.Identifier("slug"))
    cursor.execute(sqlquery, (tittle, tagline, content, date, slug))
    db.commit()


def authenticateuser(user, password):
    sqlquery = sql.SQL('SELECT * FROM users where {username} = %s AND {password} = %s;').format(
        username=sql.Identifier("username"), password=sql.Identifier("password"))
    cursor.execute(sqlquery, (user, password))
    result = cursor.fetchone()
    if result:
        return user
    else:
        return None

def editprofile(username ,name,about):
    if checkuser(username):
        sqlquery = sql.SQL('update users set {name} = %s ,{about} = %s where {username} = %s').format(
            name = sql.Identifier("name"),
            about = sql.Identifier("about"),
            username = sql.Identifier("username"))
        cursor.execute(sqlquery,(name,about,username))
        db.commit()
        return True
    else:
        return False

def signUpUser(name, email, username, password, about):
    if checkuser(username) == False:
        sqlquery = sql.SQL('insert into users ({name},{email},{username},{password},{about}) values(%s,%s,%s,%s,%s);').format(
            name=sql.Identifier("name"), email=sql.Identifier("email"), username=sql.Identifier("username"),
            password=sql.Identifier("password"),
            about = sql.Identifier("about"))
        cursor.execute(sqlquery, (name, email, username, password, about))
        db.commit()
        return True
    else:
        return False


def checkuser(username):
    array = []
    sqlquery = sql.SQL('SELECT {username} from users;').format(
        username=sql.Identifier("username"))
    cursor.execute(sqlquery)
    data = cursor.fetchall()
    for i in range(len(data)):
        array.append(data[i][0])
    if username in array:
        return True
    else:
        return False


def changePassword(userName, oldPassword, newPassword):
    sqlquery = sql.SQL('select * from users where {username} = %s and {password} = %s;').format(
        username=sql.Identifier("username"),
        password=sql.Identifier("password")
    )
    cursor.execute(sqlquery, (userName, oldPassword))
    data = cursor.fetchone()
    if data:
        if data[3] == oldPassword:
            sqlquery = sql.SQL('update users set {password} = %s where {username} = %s').format(
                password=sql.Identifier("password"),
                username=sql.Identifier("username")
            )
            cursor.execute(sqlquery, (newPassword, userName))
            db.commit()
            return True
    else:
        return False
def like_blog(slug):
    sqlquery = sql.SQL('select likes from post where {slug} = %s').format(
        slug = sql.Identifier("slug")
    )
    cursor.execute(sqlquery,(slug,))
    data = cursor.fetchone()[0]
    likes = data if data else 0
    sq = sql.SQL('update post set {likes} = %s where {slug} = %s').format(
        likes = sql.Identifier("likes"),
        slug = sql.Identifier("slug"))
    cursor.execute(sq,(int(likes)+1,slug))
    db.commit()

def unlike_blog(slug):
    sqlquery = sql.SQL('select likes from post where {slug} = %s').format(
        slug = sql.Identifier("slug")
    )
    cursor.execute(sqlquery,(slug,))
    data = cursor.fetchone()[0]
    likes = data if data else 0
    sq = sql.SQL('update post set {likes} = %s where {slug} = %s').format(
        likes = sql.Identifier("likes"),
        slug = sql.Identifier("slug"))
    cursor.execute(sq,(int(likes)-1,slug))
    db.commit()



def get_likes(username):
    sqlquery = sql.SQL('select likes from users where {username} = %s').format(username = sql.Identifier("username"))
    cursor.execute(sqlquery,(username,))
    data = cursor.fetchone()[0]
    return (list(data) if data else [])
def add_like(username,slug):
    likes = get_likes(username)
    if slug not  in likes:
        likes.append(slug)
        sqlquery = sql.SQL('update users set {likes} = %s where {username} = %s').format(
            likes = sql.Identifier("likes"),
            username = sql.Identifier("username"))
        cursor.execute(sqlquery,(likes,username))
        db.commit()
        like_blog(slug)
    else:
        likes.remove(slug)
        sqlquery = sql.SQL('update users set {likes} = %s where {username} = %s').format(
            likes = sql.Identifier("likes"),
            username = sql.Identifier("username"))
        cursor.execute(sqlquery,(likes,username))
        db.commit()
        unlike_blog(slug)

def check_liked_by_user(username,slug):
    sqlquery = sql.SQL('select likes from users where {username} = %s').format(username = sql.Identifier("username"))
    cursor.execute(sqlquery,(username,))
    data = cursor.fetchone()
    if slug in data[0]:
        return True
    else:
        return False
    
# def add_comment(slug,username,comment,date):
#     sqlquery = sql.SQL('select comment from post where {slug} = %s').format(slug = sql.Identifier("slug"))
#     cursor.execute(sqlquery,(slug,))
#     commentdata = cursor.fetchone()[0]
#     sqlquery = sql.SQL('select comment_no from post where {slug} = %s').format(slug = sql.Identifier("slug"))
#     cursor.execute(sqlquery,(slug,))
#     commentno = cursor.fetchone()[0]
    
def getComment(slug):
    sqlquery = sql.SQL('select comment from post where {slug} = %s').format(slug = sql.Identifier("slug"))
    cursor.execute(sqlquery,(slug,))
    data = cursor.fetchone()
    data = data[0] if data else []
    return utils.JsonStr(data)
def get_id(slug):
    sqlquery = sql.SQL('select comment_no from post where {slug} = %s').format(slug = sql.Identifier("slug"))
    cursor.execute(sqlquery,(slug,))
    data = cursor.fetchone()
    data = data[0] if data[0] != None else 0
    return int(data) 

def increment_id(slug):
    id = get_id(slug)+1
    sqlquery = sql.SQL('update post set {comment_no} = %s where {slug} = %s').format(
        comment_no = sql.Identifier("comment_no"),
        slug = sql.Identifier("slug"))
    cursor.execute(sqlquery,(id,slug))
    db.commit()


def add_comment(slug,username,commment_text,date):
    id = get_id(slug)
    comments = getComment(slug)
    comments.add_comment(id,username,commment_text,date)
    sqlquery = sql.SQL('update post set {comment} = %s where {slug} = %s').format(
        comment = sql.Identifier("comment"),
        slug = sql.Identifier("slug"))
    cursor.execute(sqlquery,(comments.to_string(),slug))
    db.commit()
    increment_id(slug)

def createImage(slug):
    sqlquery = sql.SQL('select image from post where {slug} = %s').format(slug = sql.Identifier("slug"))
    cursor.execute(sqlquery,(slug,))
    imageData = cursor.fetchone()
    imageData = imageData[0] if imageData else False
    if imageData:
        try:
            fopen = open(f'./static/blogimages/{slug}.jpeg','xb')
            fopen.write(imageData)
            fopen.close()
        except:
            return 
    else:
        return False

