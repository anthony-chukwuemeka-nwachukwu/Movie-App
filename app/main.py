from datetime import datetime
from email.policy import default
from flask import Flask, render_template, request
import app.backend.utils as ut_port
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
API_KEY="5d389ede"

"""DB CONFIGURATION START"""

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# basedir = '../'

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Comment Class/Model
class Comment(db.Model):
  comment_id = db.Column(db.Integer, primary_key=True)
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

"""DB CONFIGURATION ENDS"""


@app.route('/', methods=['GET'])
def index(query=False, show="Default"):
    if not query:
        query=ut_port.rand_search()
    
    genre_dict = ut_port.genries(query,API_KEY)
    
    return render_template("home.html", genres=genre_dict, query=query, show=show)

@app.route('/search', methods=['POST'])
def search():
    query = request.form['search']
        
    return index(query, "Showing for")

@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    name = request.form['name']
    email = request.form['email']
    comment = request.form['comment']
    mv_id = request.form['movie_id']
    
    new_comment = Comment(name, mv_id, comment, email)

    db.session.add(new_comment)
    db.session.commit()
    
    return movie(mv_id)


@app.route('/movie/<id>', methods=['GET'])
def movie(id):
    title, link, year, rating, runtime, genre, poster, desc, director = ut_port.single_movie(id,API_KEY)

    comments = db.session.query(Comment).filter_by(movie_id=id).all()
    comments = comments_schema.dump(comments)
    
    movies = zip(title,[id],poster,desc,director,year)
    return render_template("movie.html", movies=movies, movie_id=id, comments=comments)

