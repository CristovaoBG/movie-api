from models import Model
from psycopg2.extras import DictCursor

if __name__ == "__main__":
    _model = Model()
    movies = _model.fetch_every_movie_base_info()
    mov_n_count = [
        (m['movie_str'], _model.get_favorited_count(m['movie_str'])) for m in movies
    ]
    
    #sql_qry = "ALTER TABLE movies ADD COLUMN favorited INTEGER DEFAULT 0;;"
    sql_qry = ""
    template = "UPDATE movies SET favorited = [COUNT] WHERE movie_str = '[MOVIE]';\n"

    for item in mov_n_count:
        sql_qry = template.replace('[MOVIE]', str(item[0])).replace('[COUNT]', str(item[1]))
        with _model.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(sql_qry)
        _model.conn.commit()
        print(item[0])
    print('ok')
