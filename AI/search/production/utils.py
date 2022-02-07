import copy
import glob
import re
import pandas as pd
from num2words import num2words
from sklearn.preprocessing import StandardScaler
#from tika import parser
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
import psycopg2
from app.keys import *

from AI.search.production.feature_extraction import FeatureExtraction

nltk.download('stopwords')
nltk.download('punkt')


class Utils:

    def __init__(self):
        """
        Preprocesses document text queries
        """
        self.porter = PorterStemmer()
        self.stopwords = stopwords.words('english')

    def get_movie_descs(self):
        conn = psycopg2.connect(
            database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PW, host=POSTGRES_URL, port=POSTGRES_PORT
        )   
        conn.autocommit = True
        query = """SELECT id, name, description FROM movie"""
        movie = pd.read_sql(query, conn)
        conn.close()
        return movie



    def process_single_document(self, doc):
        """
        preprocess single document
        :param doc: str
        :return: list(str)
        """
        alpn = re.sub(r'[^a-zA-Z0-9]', ' ', doc).lower()
        tokens = nltk.word_tokenize(alpn)

        filtered_words = [self.porter.stem(word) for word in tokens if word not in self.stopwords]
        words_without_nums = []
        for word in filtered_words:
            try:
                word = num2words(word).split('-')
                words_without_nums.extend(word)
            except:
                words_without_nums.append(word)
        return words_without_nums

    def process_documents(self, data):
        
        data['text'] = data.apply(lambda x: self.process_single_document(str(x['name'])+' '+str(x['description'])), axis=1)

        return data

    def process_query(self, text):
        tokens = self.process_single_document(text)
        return tokens

    def ranked_ids(self, query, data):
        df = copy.deepcopy(data)
        
        processed_resumes = self.process_documents(df)

        featureExtraction = FeatureExtraction()
        processed_query = self.process_query(query)
        fe = featureExtraction.generate_features(processed_resumes, processed_query)

        #return fe.id.values, fe.mean_tfidf.values, fe.bm25.values, self.normalize(fe.drop(['id', 'name', 'description'], axis=1).values)

        z = [x for _,x in sorted(zip(list(fe.bm25.values) ,list(fe.id.values)), reverse=True)]

        return z




if __name__ == '__main__':
    utils = Utils()
    df=utils.get_movie_descs()
    p=utils.ranked_ids('love', df)
    print(p[:2])
