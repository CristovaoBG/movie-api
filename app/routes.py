from flask import request, jsonify
from services import Service
from models import Model
#from services import save_or_update_data

service = Service()

def configure_routes(app):
    @app.route('/api_movie_relations/', methods=['GET'])
    def get_movie_relations():
        movie_str = request.args.get('movie_str')
        return jsonify(service.get_movie_relations(movie_str))
    
    @app.route('/api_base_info/', methods=['GET'])
    def fetch_every_movie_base_info():
        movie_str = request.args.get('movie_str')
        return jsonify(service.fetch_every_movie_base_info(movie_str))
    
    @app.route('/api_movies_by_names/', methods=['GET'])
    def fetch_movies_by_names():
        movies = request.args.get('movies')
        return jsonify(service.fetch_movies_by_names(movies))

    @app.route('/')
    def debug_deploy():
        return 'online'
