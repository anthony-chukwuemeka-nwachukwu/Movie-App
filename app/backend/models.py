from datetime import datetime
from app import db
from sqlalchemy.dialects.postgresql import JSON


class Comment(db.Model):

    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_name = db.Column(db.String(), nullable=False)
    movie_id = db.Column(db.String(), nullable=False)
    comment = db.Column(db.String())
    user_email = db.Column(db.String(), nullable=False)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)

    def __init__(self, user_name, movie_id, comment, user_email):
        self.user_name = user_name
        self.movie_id = movie_id
        self.comment = comment
        self.user_email = user_email
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()

    def __repr__(self):
        return '<id {}>'.format(self.id)


class User(db.Model):

    __tablename__ = 'users'
    email= db.Column(db.String(64), primary_key=True, unique=True, nullable=False)
    name= db.Column(db.String(64), unique=False, nullable=False)
    password= db.Column(db.String(64), unique=False, nullable=False)
    likes= db.Column(db.String(64), unique=False, nullable=True)

    def __init__(self, email, name, password, likes):
        
        self.email = email
        self.name = name
        self.password = password
        self.likes = likes
    
    def __repr__(self):
        return '<email {}>'.format(self.email)

class Movie(db.Model):

    __tablename__ = 'movies'
    id= db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name= db.Column(db.String(), unique=False, nullable=False)
    description= db.Column(db.String(), unique=False, nullable=True)
    link= db.Column(db.String(), unique=False, nullable=False)
    poster= db.Column(db.String(), unique=False, nullable=True)
    # genre_id = db.Column(db.String(64), db.ForeignKey('genre.id'))

    def __init__(self, id, name, link, description="", poster=""):
        
        self.id = id
        self.name = name
        self.link = link
        self.poster = poster
        self.description = description

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Genre(db.Model):

    __tablename__ = 'genres'
    id= db.Column(db.Integer, primary_key=True, unique=True)
    name= db.Column(db.String(64), unique=False, nullable=False)
    movie_id= db.Column(db.String(64), unique=False, nullable=False)
    # movies = db.relationship("Movie", backref="genre", lazy=True)

    def __init__(self,movie_id, name=""):
        
        self.movie_id = movie_id
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)
        
class LikedMovies(db.Model):

    __tablename__ = 'genres'
    id= db.Column(db.Integer, primary_key=True, unique=True)
    user_id= db.Column(db.String(64), unique=False, nullable=False)
    movie_id= db.Column(db.String(64), unique=False, nullable=False)

    def __init__(self,movie_id, user_id):
        
        self.movie_id = movie_id
        self.user_id = user_id

    def __repr__(self):
        return '<id {}>'.format(self.id)