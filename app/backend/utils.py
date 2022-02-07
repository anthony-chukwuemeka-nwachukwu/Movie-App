from datetime import datetime
import gzip
import os
import random
import shutil
import requests
import numpy as np
import urllib.request

def single_movie(ID, API_KEY):
    URL = "http://www.omdbapi.com/?i={}&apikey={}".format(ID, API_KEY)
    r = requests.get(URL)
    json = r.json()

    title, link, year, rating, runtime, genre, poster, desc, director = [json['Title']], [json['Poster']], [json['Year']],\
        [json['Rated']], [json['Runtime']], \
        [json['Genre']], [json['Poster']], [json['Plot']], [json['Director']]
    return title, link, year, rating, runtime, genre, poster, desc, director


def genries(query, API_KEY):
    
    URL = "http://www.omdbapi.com/?s={}&apikey={}".format(query, API_KEY)

    r = requests.get(URL)
    json = r.json()
    
    genre_dict = {}

    if json['Response'] == 'True' or json['Response'] == True:
        search_result = json['Search']
        for movie in search_result:
            
            _, _, _, _, _, genre_list, _, _, _ = single_movie(movie['imdbID'],API_KEY)

            for genre in genre_list[0].split(","):
                if genre in genre_dict.keys():
                    genre_dict[genre][0].append(movie['Poster'])
                    genre_dict[genre][1].append(movie['Type'])
                    genre_dict[genre][2].append(movie['imdbID'])
                    genre_dict[genre][3].append(movie['Title'])
                else:
                    genre_dict[genre] = [[],[],[],[]]
    gen = []
    for k,v in genre_dict.items():
        gen.append([k,np.array(v,dtype=object).T])
    return gen

def rand_search():
    searches = ["love", "game", "biography", "science", "hate", "trouble", "care", "romance", "crime", "high school"]
    rand = random.randint(0,9)
    return  searches[rand]

def download():
    
    data_path = 'app/backend/data/'
    urllib.request.urlretrieve('https://datasets.imdbws.com/title.ratings.tsv.gz', data_path+'title.tsv.gz')

    with gzip.open(data_path+'title.tsv.gz', 'rb') as f:
        data = f.readlines()

    data = [f.decode("utf-8").split('\t')[0] for f in data]

    return data[::-1]
"""
if __name__ == "__main__":
    print(download())"""