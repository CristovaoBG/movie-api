import psycopg2
from psycopg2.extras import DictCursor
import os
import json
from itertools import chain
from utils import read_list_file
from collections import Counter
import threading

DB_CONN_FILE_PATH = './db_connection.json'
USER_FAV_FILE_PATH = "./data/users_favourites.bin"

class Model:
    conn = None
    _instance = None
    _users_favourites_list = None
    _count_dict = None
    _lock = threading.Lock()

    # thread safe singleton
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        try:
            with open(DB_CONN_FILE_PATH, 'r') as file:
                conn_data = json.load(file)
            self.conn = psycopg2.connect(
                host=conn_data['host'],
                dbname=conn_data['dbname'],
                user=conn_data['user'],
                password=conn_data['password'],
                port=conn_data['port']
            )
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
        try:
            self.users_favourites_list = read_list_file(USER_FAV_FILE_PATH)
            favorites_concat = []
            for user, favorites in self.users_favourites_list:
                favorites_concat += favorites
            self._count_dict = Counter(favorites_concat)
        except Exception as e:
            print(f"Erro ao ler favoritos: ", e)

    def get_users_favorites_list(self):
        return self.users_favourites_list
    
    def get_favorited_count(self, movie_str):
        return self._count_dict[movie_str]

    def fetch_every_movie_base_info(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("""
            SELECT movie_str, movie_name, movie_name_en, year, url_img
            FROM movies
            """)
            return [dict(row) for row in cursor.fetchall()]

    # uso?    
    def fetch_one_movie_by_name(self, name: str):
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("""
            SELECT *
            FROM movies
            WHERE movie_name = %s OR movie_name_en = %s
            """, (name, name))
            result = cursor.fetchone()
            return dict(result)
            
    def fetch_movies_by_names(self, names: list):
        placeholders = ', '.join(['%s'] * len(names))
        query = f"""
            SELECT *
            FROM movies
            WHERE movie_str IN ({placeholders})
        """
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query, tuple(names))
            results = cursor.fetchall()
            return [dict(result) for result in results]
            
    def search_movie_name(self, search_string: str):
        query = """
            SELECT *
            FROM movies
            WHERE UPPER(movie_name) LIKE UPPER(%s) OR UPPER(movie_name_en) LIKE UPPER(%s)
        """
        search_param = f"%{search_string}%"
        
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query, (search_param, search_param)) 
            results = cursor.fetchall()
            return [dict(result) for result in results]


if __name__ == "__main__":
    model = Model()
    #k = model.fetch_movies_by_names(["superbad-e-hoje-t3581"])
    k = model.fetch_every_movie_base_info()
    print(k)