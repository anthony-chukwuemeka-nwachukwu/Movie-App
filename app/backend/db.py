from datetime import datetime
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import uuid


app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
basedir = '../'

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Comment Class/Model
class Comment(db.Model):
  comment_id = db.Column(db.String(32), primary_key=True, default=str(uuid.uuid4()), nullable=False)
  user_name = db.Column(db.String(100), nullable=False)
  movie_id = db.Column(db.String(100), nullable=False)
  comment = db.Column(db.String(200))
  user_email = db.Column(db.String(100), nullable=False)
  createdAt = db.Column(db.DateTime)
  updatedAt = db.Column(db.DateTime)

  def __init__(self, user_name, movie_id, comment, user_email):
    self.user_name = user_name
    self.movie_id = movie_id
    self.comment = comment
    self.user_email = user_email
    self.createdAt = datetime.now()
    self.updatedAt = datetime.now()

# Todo Schema
class CommentSchema(ma.Schema):
  class Meta:
    fields = ('comment_id', 'user_name', 'movie_id', 'comment', 'user_email', 'createdAt', 'updatedAt')

# Init schema
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)

# Execute only once
#db.create_all()