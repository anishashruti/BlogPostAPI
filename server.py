#We are creating an BLOGAPI

from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import linkedlist
import hashtable
import random
import binarysearchtree

# app
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0

# configure sqlite3 to enforce foreign key constraints
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


db = SQLAlchemy(app) #creating instance of the database/SqlAlchemy class (connecting the orm with our flask application)
now = datetime.now() #for updating date values in the tables

# models

#a table for users
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    posts = db.relationship("BlogPost", cascade="all, delete")

#a table for blog post
class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

# routes
# route is: when a url rule(/user) is appended to the url the create_user function is called (if it is a post request)
@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json() #variable to store the requested data
    #the get_json parses the request as a json allowing us to access the key
    new_user = User(
        name=data["name"],
        email=data["email"],
        address=data["address"],
        phone=data["phone"],
    )
    db.session.add(new_user)
    db.session.commit()
    #returning a response and the status code for the response
    return jsonify({"message": "User created"}), 200

#for descending order we are going to make use of linked list insert at the beginning
@app.route("/user/descending_id", methods=["GET"])
def get_all_users_descending():
    users=User.query.all()
    usersll=linkedlist.LinkedList()
    for user in users:
        usersll.insert_front(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )

    return jsonify(usersll.to_list()), 200

#For ascending order we are going to use linkedlist insert at end
@app.route("/user/ascending_id", methods=["GET"])
def get_all_users_ascending():
    users=User.query.all()
    usersll=linkedlist.LinkedList()
    for user in users:
        usersll.insert_end(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )

    return jsonify(usersll.to_list()), 200


@app.route("/user/<user_id>", methods=["GET"])
def get_one_user(user_id):
    users = User.query.all()

    all_users_ll = linkedlist.LinkedList()

    for user in users:
        all_users_ll.insert_front(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )
    user = all_users_ll.get_user_by_id(user_id)

    return jsonify(user), 200

@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify({}), 200

@app.route("/blog_post/<user_id>", methods=["POST"])
def create_blog_post(user_id):
    data = request.get_json()
    #we are going to verify the user, if this is not validated we may end up in foriegn key constrains
    user = User.query.filter_by(id=user_id).first()
    if not user:
        #status code 400 meas client sends a bad request
        return jsonify({"message":"User doesnot exist"}),400
    print(user.name)
    ht = hashtable.Hashtable(10)
    ht.add_key_value("title", data["title"])
    ht.add_key_value("body", data["body"])
    ht.add_key_value("date", now)
    ht.add_key_value("user_id", user_id)

    ht.print_table()

    #creating a blogpost instance
    new_blog_post = BlogPost(
        title=ht.get_value("title"),
        body=ht.get_value("body"),
        date=ht.get_value("date"),
        user_id=ht.get_value("user_id"),
    )
    db.session.add(new_blog_post)
    db.session.commit()
    return jsonify({"message": "new blog post created"}), 200

@app.route("/blog_post/<blog_post_id>", methods=["GET"])
def get_one_blog_post(blog_post_id):
    blog_posts = BlogPost.query.all()
    #to avoid the linear insertion
    random.shuffle(blog_posts) # random binary tree have a better chance of balanced tree structure

    bst=binarysearchtree.BinarySearchTree()

    for post in blog_posts:
        bst.insert({
            "id" : post.id,
            "title" : post.title,
            "body" : post.body,
            "user_id" : post.user_id,
        })

    post = bst.search(blog_post_id)

    if not post:
        return jsonify({"message": "post not found"})

    return jsonify(post)

@app.route("/blog_post/numeric_body", methods=["GET"])
def get_numeric_post_bodies():
    pass

@app.route("/blog_post/delete_last_10", methods=["DELETE"])
def delete_last_10():
    pass


# if we are running our server.py file as a main application(eg: python  server.py {the internal variable __main__ will be set}) the we have to start the app in debug mode
if __name__ == "__main__":
    app.run(debug=True)