from flask import request, jsonify
from services import Service
from models import Model
#from services import save_or_update_data

service = Service()

def configure_routes(app):
    @app.route('/api/movie-relations/', methods=['GET'])
    def get_movie_relations():
        movie_str = request.args.get('movie_str')
        return jsonify(service.get_movie_relations(movie_str))
    
    @app.route('/api/base-info/', methods=['GET'])
    def fetch_every_movie_base_info():
        return jsonify(service.fetch_every_movie_base_info())
    
    @app.route('/api/movies-by-names/', methods=['GET'])
    def fetch_movies_by_names():
        movies :dict = request.get_json()
        movie_list = movies.get('movies')
        return jsonify(service.fetch_movies_by_names(movie_list))
    
    @app.route('/api/search-movie-name/', methods=['GET'])
    def search_movie_name():
        search_str = request.args.get('value')
        return jsonify(service.search_movie_name(search_str))

    @app.route('/')
    def debug_deploy():
        return 'online'
