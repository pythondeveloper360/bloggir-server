import psycopg2
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
    sqlquery = "SELECT * FROM post"
    cursor.execute(sqlquery)
    data = cursor.fetchall()
    # print(data)
    for i in range(len(data)):
        array.append(dict(id=data[i][0], tittle=data[i][1], tagline=data[i][2], content=data[i]
                          [3], slug=data[i][4], date=data[i][5], author=data[i][6], authorusername=data[i][7]))
    return array


def insertPost(tittle, tagline, content, slug, date, author, authorusername):
    rsqlquery = "INSERT INTO post (tittle,tagline,content,slug,date,author,authorusername) values ('{}','{}','{}','{}','{}','{}','{}'); ".format(
        tittle, tagline, content, slug, date, author, authorusername)
    sqlquery = r'{}'.format(rsqlquery)

    cursor.execute(sqlquery)
    db.commit()


def readPostBySlug(slug):
    sqlquery = """SELECT * FROM post where "slug" = '{}';""".format(slug)
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
    sqlquery = """SELECT * FROM post where "authorusername" = '{}';""".format(
        authorusername)
    cursor.execute(sqlquery)
    data = cursor.fetchall()
    for i in range(len(data)):
        array.append(dict(id=data[i][0], tittle=data[i][1], tagline=data[i][2], content=data[i]
                          [3], slug=data[i][4], date=data[i][5], author=data[i][6], authorusername=data[i][7]))
    return array


def getAuthorUserName(slug):
    sqlquery = """SELECT authorusername from post where "slug" = '{}';""".format(
        slug)
    cursor.execute(sqlquery)
    data = cursor.fetchone()
    return data if data else "no user"


def getNameFromUserName(username):
    sqlquery = '''select name from "users" where "username" = '{}';'''.format(
        username)
    cursor.execute(sqlquery)
    data = cursor.fetchone()
    if data:
        return data[0]
    else:
        return False


def deletePost(slug):
    sqlquery = """DELETE FROM post WHERE "slug" = '{}';""".format(slug)
    cursor.execute(sqlquery)
    db.commit()


def updatePost(tittle, tagline, content, slug, date):
    rsqlquery = """UPDATE post set tittle = '{}', tagline = '{}', content = '{}', date = '{}' WHERE slug = '{}';""".format(
        tittle, tagline, content, date, slug)
    sqlquery = r'{}'.format(rsqlquery)
    cursor.execute(sqlquery)
    db.commit()




def authenticateuser(user, password):
    sqlquery = """SELECT * FROM users where "username" = '{}' AND "password" = '{}';""".format(
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
    sqlquery = """SELECT "email" from users;"""
    cursor.execute(sqlquery)
    data = cursor.fetchall()
    for i in range(len(data)):
        array.append(data[i][0])
    if email in array:
        return True
    else:
        return False
