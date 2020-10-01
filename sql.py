import psycopg2
from psycopg2 import sql
import json
import os


# db = sqlite3.connect("db.sqlite3", check_same_thread=False)
# db = psycopg2.connect(user=str(os.getenv('username')),
#                       password=str(os.getenv('password')),
#                       host=str(os.getenv('host')),
#                       port=str(os.getenv('port')),
#                       database=str(os.getenv('database')))
db = psycopg2.connect(
    user='xubuuanpszwwcx',
    password='3e2b69885d81e646182281d1cfb60ed02a6a584d24b62ba81f4734f1ed8c5e2c',
    host='ec2-54-197-254-117.compute-1.amazonaws.com',
    port='5432',
    database='dffngl3u0qkkld'
)
# db = psycopg2.connect(user = "postgres",
#                       password = 'qsa-1299',
#                       host = "localhost",
#                       port = '5432',
#                       database = 'postgres'  )
cursor = db.cursor()

""""
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
    sqlquery = sql.SQL("SELECT * FROM post")
    cursor.execute(sqlquery)
    data = cursor.fetchall()
    # print(data)
    for i in range(len(data)):
        array.append(dict(id=data[i][0], tittle=data[i][1], tagline=data[i][2], content=data[i]
                        [3], slug=data[i][4], date=data[i][5], author=data[i][6], authorusername=data[i][7]))
    return array


def insertPost(tittle, tagline, content, slug, date, author, authorusername):
    sqlquery = sql.SQL('INSERT INTO post ({tittle},{tagline},{content},{slug},{date},{author},{authorusername}) values (%s,%s,%s,%s,%s,%s,%s);').format(
        tittle=sql.Identifier("tittle"), tagline=sql.Identifier("tagline"), content=sql.Identifier("content"), slug=sql.Identifier("slug"), date=sql.Identifier("date"), author=sql.Identifier("author"), authorusername=sql.Identifier("authorusername"))

    cursor.execute(sqlquery, (tittle, tagline, content,
                            slug, date, author, authorusername))
    db.commit()


def readPostBySlug(slug):
    sqlquery = sql.SQL(
        'SELECT * FROM post where {slug} = %s;').format(slug=sql.Identifier("slug"))
    cursor.execute(sqlquery, (slug,))
    data = cursor.fetchone()
    return dict(id=data[0], tittle=data[1], tagline=data[2], content=data
                [3], slug=data[4], date=data[5], author=data[6], authorusername=data[7])


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
    sqlquery = sql.SQL('SELECT * FROM post where {authorusername} = %s;').format(
        authorusername=sql.Identifier("authorusername"))
    cursor.execute(sqlquery, (authorusername,))
    data = cursor.fetchall()
    for i in range(len(data)):
        array.append(dict(id=data[i][0], tittle=data[i][1], tagline=data[i][2], content=data[i]
                        [3], slug=data[i][4], date=data[i][5], author=data[i][6], authorusername=data[i][7]))
    return array

def informationByusername(username):
    re = {}
    sqlquery = sql.SQL('select * from users where {username} = %s').format(
        username = sql.Identifier("username")
    )
    cursor.execute(sqlquery,(username,))
    data = cursor.fetchall()
    re = {"name":data[0][0],"email":data[0][1],"username":data[0][2]} if data else False
    return re


def getAuthorUserName(slug):
    sqlquery = sql.SQL('SELECT authorusername from post where {slug} = %s;').format(
        slug=sql.Identifier("slug"))
    cursor.execute(sqlquery, slug)
    data = cursor.fetchone()
    return data if data else "no user"


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


def signUpUser(name, email, username, password):
    if checkuser(username) == False:
        sqlquery = sql.SQL('insert into users ({name},{email},{username},{password}) values(%s,%s,%s,%s);').format(
            name=sql.Identifier("name"), email=sql.Identifier("email"), username=sql.Identifier("username"), password=sql.Identifier("password"))
        cursor.execute(sqlquery, (name, email, username, password))
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
    cursor.execute(sqlquery,(userName,oldPassword))
    data = cursor.fetchone()
    if data:
        if data[3] == oldPassword:
            sqlquery = sql.SQL('update users set {password} = %s where {username} = %s').format(
                password = sql.Identifier("password"),
                username = sql.Identifier("username")
            )
            cursor.execute(sqlquery,(newPassword,userName))
            db.commit()
            return True
    else:
        return False
        