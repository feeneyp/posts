import json

from flask import request, Response, url_for
from jsonschema import validate, ValidationError

import models
import decorators
from posts import app
from database import session

  
@app.route("/api/posts", methods=["GET"])
@decorators.accept("application/json")
def posts_get():
    """ Get a list of posts """
    # Get the querystring arguments
    title_like = request.args.get("title_like")
    body_like = request.args.get("body_like")

    # Get and filter the posts from the database
    posts = session.query(models.Post)
    if title_like and body_like:
        posts = posts.filter(models.Post.title.contains(title_like))
        posts = posts.filter(models.Post.body.contains(body_like))
    posts = posts.all()

    # Convert the posts to JSON and return a response
    data = json.dumps([post.as_dictionary() for post in posts])
    return Response(data, 200, mimetype="application/json")
  

  
@app.route("/api/posts", methods=["POST"])
@decorators.accept("application/json")
def posts_post():
    """ Add a new post """
    data = request.json

    # Add the post to the database
    post = models.Post(title=data["title"], body=data["body"])
    session.add(post)
    session.commit()

    # Return a 201 Created, containing the post as JSON and 
    #according to the tutorial with the
    #Location header set to the location of the post
    #but that gives an error so I commented it out
    data = json.dumps(post.as_dictionary())
    headers = {"Location": url_for("posts_get")}   #, id=post.id)}
    return Response(data, 201, headers=headers,
                    mimetype="application/json")
  
  
@app.route("/api/edit/<id>", methods=["PUT"])
@decorators.accept("application/json")
def posts_put(id):
    """ Update an existing post """
    data = request.json

    # Update the post in the database
    post = session.query(models.Post).get(id)
    if not post:
      return Response('Not Found', status=404)
    post.title=data["title"]
    post.body=data["body"]
    session.commit()
    # Return a 201 Created, containing the post as JSON and 
    #according to the tutorial with the
    #Location header set to the location of the post
    #but that gives an error so I commented it out
    data = json.dumps(post.as_dictionary())
    headers = {"Location": url_for("posts_get")}   #, id=post.id)}
    return Response(data, 201, headers=headers,
                    mimetype="application/json")
  