from datetime import datetime
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app.keys import *

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
"""POSTGRES_USER='postgres'
POSTGRES_PW='azubuike12'
POSTGRES_URL='localhost'
POSTGRES_DB='moviedb'
POSTGRES_PORT=5432"""

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}:{}/{}'.format(POSTGRES_USER,POSTGRES_PW,POSTGRES_URL,POSTGRES_PORT,POSTGRES_DB)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Class/Model

class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(250), nullable=False)
    movie_id = db.Column(db.String(), nullable=False)
    comment = db.Column(db.String(250))
    user_email = db.Column(db.String(250), nullable=False)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)

    def __init__(self, user_name, movie_id, comment, user_email):
        self.user_name = user_name
        self.movie_id = movie_id
        self.comment = comment
        self.user_email = user_email
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()


class User(db.Model):

    email= db.Column(db.String(250), primary_key=True, unique=True, nullable=False)
    name= db.Column(db.String(250), unique=False, nullable=False)
    password= db.Column(db.String(250), unique=False, nullable=False)
    likes= db.Column(db.String(250), unique=False, nullable=True)

    def __init__(self, email, name, password, likes):
        
        self.email = email
        self.name = name
        self.password = password
        self.likes = likes

class Movie(db.Model):

    id= db.Column(db.String(), primary_key=True, unique=True, nullable=False)
    name= db.Column(db.String(), unique=False, nullable=False)
    description= db.Column(db.String(), unique=False, nullable=True)
    link= db.Column(db.String(), unique=False, nullable=False)
    poster= db.Column(db.String(), unique=False, nullable=True)
    year= db.Column(db.Integer, unique=False, nullable=True)
    director= db.Column(db.String(), unique=False, nullable=True)
    # genre_id = db.Column(db.String(64), db.ForeignKey('genre.id'))

    def __init__(self, id, name, link, description, poster, year, director):
        
        self.id = id
        self.name = name
        self.link = link
        self.poster = poster
        self.description = description
        self.year = year
        self.director = director

class Genre(db.Model):

    id= db.Column(db.Integer, primary_key=True, unique=True)
    name= db.Column(db.String(), unique=False, nullable=False)
    movie_id= db.Column(db.String(), unique=False, nullable=False)
    # movies = db.relationship("Movie", backref="genre", lazy=True)

    def __init__(self,movie_id, name=""):
        
        self.movie_id = movie_id
        self.name = name
        
class LikedMovies(db.Model):

    id= db.Column(db.Integer, primary_key=True, unique=True)
    user_id= db.Column(db.String(), unique=False, nullable=False)
    movie_id= db.Column(db.String(), unique=False, nullable=False)

    def __init__(self,movie_id, user_id):
        
        self.movie_id = movie_id
        self.user_id = user_id

# Schema
class CommentSchema(ma.Schema):
  class Meta:
    fields = ('comment_id', 'user_name', 'movie_id', 'comment', 'user_email', 'createdAt', 'updatedAt')
class UserSchema(ma.Schema):
  class Meta:
    fields = ('email', 'name', 'password', 'likes')
class MovieSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'link', 'description', 'poster', 'year', 'director')
class GenreSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'movie_id')
class LikedMoviesSchema(ma.Schema):
  class Meta:
    fields = ('id', 'user_id', 'movie_id')

# Init schema
comment_schema = CommentSchema()
comment_schemas = CommentSchema(many=True)

user_schema = UserSchema()
user_schemas = UserSchema(many=True)

movie_schema = MovieSchema()
movie_schemas = MovieSchema(many=True)

genre_schema = GenreSchema()
genre_schemas = GenreSchema(many=True)

likedMovies_schema = LikedMoviesSchema()
likedMovies_schemas = LikedMoviesSchema(many=True)

# Execute only once
#db.create_all()