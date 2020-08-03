import psycopg2
import json
import os


# db = sqlite3.connect("db.sqlite3", check_same_thread=False)
db = psycopg2.connect(user = str(os.getenv('username')),
                                  password = str(os.getenv('password')),
                                  host = str(os.getenv('host')),
                                  port = str(os.getenv('port')),
                                  database = str(os.getenv('database')))
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


def readAllPostsWithLimit(limit):
    array = []
    sqlquery = "SELECT * FROM post limit  '{}';".format(limit)
    cursor.execute(sqlquery)
    data = cursor.fetchall()
    # print(data)
    for i in range(len(data)):
        array.append(dict(id=data[i][0], tittle=data[i][1], tagline=data[i][2], content=data[i]
                          [3], slug=data[i][4], date=data[i][5], author=data[i][6], authorusername=data[i][7]))
    return array


def readAllPosts():
    array = []
    sqlquery = "SELECT * FROM post"
    cursor.execute(sqlquery)
    data = cursor.fetchall()
    # print(data)
    for i in range(len(data)):
        array.append(dict(id=data[i][0], tittle=data[i][1], tagline=data[i][2], content=data[i]
                          [3], slug=data[i][4], date=data[i][5], author=data[i][6], authorusername=data[i][7]))
    return array


def insertPost(tittle, tagline, content, slug, date, author, authorusername):
    sqlquery = "INSERT INTO post (tittle,tagline,content,slug,date,author,authorusername) values ('{}','{}','{}','{}','{}','{}','{}'); ".format(
        tittle, tagline, content, slug, date, author, authorusername)
    cursor.execute(sqlquery)
    db.commit()


def readPostBySlug(slug):
    sqlquery = "SELECT * FROM post where slug = '{}';".format(slug)
    cursor.execute(sqlquery)
    data = cursor.fetchone()
    return dict(id=data[0], tittle=data[1], tagline=data[2], content=data
                [3], slug=data[4], date=data[5], author=data[6], authorusername=data[7])


def slugs():
    array = []
    sqlquery = "SELECT slug from post;"
    cursor.execute(sqlquery)
    data = cursor.fetchall()
    for i in range(len(data)):
        array.append(data[i][0])
    return array



def readAllPostsByAuthor(authorusername):
    array = []
    sqlquery = "SELECT * FROM post where authorusername = '{}';".format(
        authorusername)
    cursor.execute(sqlquery)
    data = cursor.fetchall()
    for i in range(len(data)):
        array.append(dict(id=data[i][0], tittle=data[i][1], tagline=data[i][2], content=data[i]
                          [3], slug=data[i][4], date=data[i][5], author=data[i][6], authorusername=data[i][7]))
    return array


def getAuthorUserName(slug):
    sqlquery = "SELECT authorusername from post where slug = '{}';".format(slug)
    cursor.execute(sqlquery)
    data = cursor.fetchone()[0]
    return data if data else "no user"


def deletePost(slug):
    sqlquery = "DELETE FROM post WHERE slug = '{}';".format(slug)
    cursor.execute(sqlquery)
    db.commit()


def updatePost(tittle, tagline, content, slug, date):
    sqlquery = "UPDATE post set tittle = '{}', tagline = '{}', content = '{}', date = '{}' WHERE slug = '{}';".format(
        tittle, tagline, content, date,slug)
    cursor.execute(sqlquery)
    db.commit()


def insertMessage(name, email, msg):
    sqlquery = "INSERT into msg(name,email,msg) values('{}','{}','{}');".format(
        name, email, msg)
    cursor.execute(sqlquery)
    db.commit()


def readAllMsg():
    array = []
    sqlquery = "SELECT * FROM msg;"
    cursor.execute(sqlquery)
    result = cursor.fetchall()
    for i in range(len(result)):
        array.append(
            dict(name=result[i][0], email=result[i][1], msg=result[i][2]))
    return array


def deleteMsg(id):
    sqlquery = "delete from msg where id = '{}';".format(id)
    db.execute(sqlquery)
    db.commit()


def authenticateuser(user, password):
    sqlquery = "SELECT * FROM users where username = '{}' AND password = '{}';".format(
        user, password)
    cursor.execute(sqlquery)
    result = cursor.fetchone()
    if result:
        return user
    else:
        return None


def signUpUser(name, email, username, password):
    sqlquery = "insert into users (name,email,username,password) values('{}','{}','{}','{}');".format(
        name, email, username, password)
    cursor.execute(sqlquery)
    db.commit()
def checkuser(email):
    array = []
    sqlquery = "SELECT email from users;"
    cursor.execute(sqlquery)
    data = cursor.fetchall()
    for i in range(len(data)):
        array.append(data[i][0])
    if email in array:
        return True
    else:
        return False
