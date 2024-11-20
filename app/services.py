from utils import read_list_file
from collections import OrderedDict, defaultdict, Counter
from models import Model
import threading

class Service:

    _model = Model()
    _lock = threading.Lock()
    _instance = None

    # thread safe singleton
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                cls._instance = super().__new__(cls)
        return cls._instance
    
    def f(x, size):
        # funcao que cresce exponencialmente a partir do valor de k, 
        # usada pra penalizar usuários com quantidade de favoritos
        # maior que o usuário em questão.
        k = size
        b = 2
        return 1 + b**(x-k)

    def get_users_similarity(self, user_name):
        users_fav = {u[0]: set(u[1]) for u in self._model.get_users_favorites_list()}
        userf = users_fav.pop(user_name)
        score_dict = {}
        for key in users_fav:
            num = len(userf & users_fav[key])
            den = len(users_fav[key])
            score_dict[key] = num/self.f(den, len(userf))
        score_dict = OrderedDict(sorted(score_dict.items(), key=lambda item: item[1], reverse=True))
        return score_dict

    def get_movie_relations(self, movie_name, expoent = 0.55):
        dd = defaultdict(float)
        for user, favorites in self._model.get_users_favorites_list():
            if movie_name in favorites:
                for other in favorites:
                    #dd[other] += 1/(count_dict[other]**0.55)
                    dd[other] += self._model.get_favorited_count(other)**-expoent
        score_dict = OrderedDict(sorted(dict(dd).items(), key=lambda item: item[1], reverse=True))
        score_dict.pop(movie_name)
        return(score_dict)
    
    def fetch_every_movie_base_info(self):
        return self._model.fetch_every_movie_base_info()
    
    def fetch_movies_by_names(self, names: list):
        return self._model.fetch_movies_by_names(names)
    
    def search_movie_name(self, names: list):
        return self._model.search_movie_name(names)

if __name__ == "__main__":
    user = "dj_crissi"
    movie = "planeta-fantastico-t14651"
    service = Service()
    #similarity_list = get_users_similarity(user)
    #print(f"Usuários similares ao usuário {user}:")
    #for key in list(similarity_list)[:10]: print(f"\t{key}: {similarity_list[key]}")
    movie_similarity = service.get_movie_relations(movie)
    print(f"Filmes similares ao filme {movie}")
    for other_movie, score in list(movie_similarity.items())[:10]: print(f"\t{other_movie}: {score}")