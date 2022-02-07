from flask import jsonify, render_template, request
import app.backend.utils as ut_port
from app.backend.db import *
from app.keys import *
from app.backend.querydb import query_movie, get_movie_by_id

API_KEY=IMDB_API_KEY


@app.route('/', methods=['GET'])
def index(query=False, show="Default", no=12):
    if not query:
        query=ut_port.rand_search()
    genres=query_movie(query, no)
        
    
    #genre_dict = ut_port.genries(query,API_KEY)
    
    return render_template("home.html", genres=genres, query=query, show=show)

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
    #title, link, year, rating, runtime, genre, poster, desc, director = ut_port.single_movie(id,API_KEY)
    genre, movie_detail = get_movie_by_id(id)

    comments = db.session.query(Comment).filter_by(movie_id=id).all()
    
    #movies = zip(title,[id],poster,desc,director,year)
    return render_template("movie.html", movies=movie_detail, genre=genre, movie_id=id, comments=comments)


@app.route('/populateDB', methods=['POST'])
def populateDB(API_KEY):
    movie_id = db.session.query(Movie.id).all()
    movie_id = [d['id'] for d in movie_schemas.dump(movie_id)]
    info = ut_port.download()
    
    for i,id in enumerate(info):

        if id not in movie_id:
        
            try:
                
                title, link, year, rating, runtime, genre, poster, desc, director = ut_port.single_movie(id,API_KEY)
                new_movie = Movie(id, title[0], link[0], desc[0], poster[0], int(year[0]), director[0])
                db.session.add(new_movie)
                
                for g in genre[0].split(','):
                    new_genre = Genre(id, g.strip())
                    db.session.add(new_genre)
                db.session.commit()
            except:
                pass
        if i /20 == 0:
            print('{}/{}'.format(i,len(info)))
    return {'response':200}


if __name__ == "__main__":
    # Execute only once
    #db.drop_all()
    #db.create_all()
    #populateDB(API_KEY)
    index()