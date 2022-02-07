import psycopg2
from AI.search.production.utils import Utils
from app.keys import *
import pandas as pd
from pandas.api.types import CategoricalDtype



def query_movie(query,no):

    conn = psycopg2.connect(
    database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PW, host=POSTGRES_URL, port=POSTGRES_PORT
)
    conn.autocommit = True
    cursor = conn.cursor()

    #Get movies by genre
    query_genre = '''SELECT DISTINCT name FROM genre'''

    cursor.execute(query_genre)
    all_genre = cursor.fetchall()
    all_genre = [e[0] for e in all_genre]

    movie_by_genre = lambda x: '''
    WITH movie_table AS
    (
        SELECT m.*, g.name AS genre_name
        FROM movie AS m
        JOIN genre g ON g.movie_id = m.id
    )
    SELECT * FROM movie_table
    WHERE genre_name = '{}'
    '''.format(x)
    #title, link, year, rating, runtime, genre, poster, desc, director
    movie_genre = []
    for i in all_genre:
        #cursor.execute(movie_by_genre(i))
        #movie_genre.append(cursor.fetchmany(no))
        df = pd.read_sql(movie_by_genre(i), conn)

        utils = Utils()        
        rank=utils.ranked_ids(query, df)
        
        id_order = CategoricalDtype(rank, ordered=True)
        df['id'] = df['id'].astype(id_order)
        df = df.sort_values('id')

        movie_genre.append(df.head(no).values)

    conn.commit()
    conn.close()

    return movie_genre

def get_movie_by_id(ID):

    conn = psycopg2.connect(
        database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PW, host=POSTGRES_URL, port=POSTGRES_PORT
    )   
    conn.autocommit = True
    cursor = conn.cursor()

    #Get movie by id
    query_genre = """SELECT name FROM genre WHERE movie_id='{}'""".format(ID)

    cursor.execute(query_genre)
    movie_genres = cursor.fetchall()

    movie_genres = [e[0] for e in movie_genres]
    

    movie = """SELECT * FROM movie WHERE id='{}'""".format(ID)
    cursor.execute(movie)
    movie_details = cursor.fetchone()

    conn.commit()
    conn.close()

    return movie_genres, movie_details

#get_movie_by_id('tt9916720')
#print(query_movie(1))