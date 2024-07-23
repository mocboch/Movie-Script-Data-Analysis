import psycopg2
import pandas as pd
import numpy as np
import warnings
def ScriptsAndGenres():
    warnings.filterwarnings("ignore")
    conn = psycopg2.connect(dbname='bechdel_test', user='postgres', password='guest')
    cur = conn.cursor()

    cur.execute('SELECT * FROM imsdb_scripts JOIN bechdel_ratings ON imsdb_scripts.imdb_id = bechdel_ratings.imdb_id JOIN tmdb_data ON tmdb_data.imdb_id = imsdb_scripts.imdb_id;')
    data = pd.DataFrame(cur.fetchall())
    df = data.copy()
    df.set_index(0, inplace=True)

    cur.execute('SELECT genre.imdb_id, genre FROM genre JOIN imsdb_scripts ON imsdb_scripts.imdb_id = genre.imdb_id;')
    genre = pd.DataFrame(cur.fetchall())
    cur.close()
    conn.close()
    for genre_ in genre[1].unique():
        df[genre_] = pd.Series()
    for row in genre.iterrows():
        df[row[1][1]][row[1][0]] = 1
    df.rename(columns={0:'imdb_id',
                            1:'script_date',
                            2:'script',
                            3:'bechdel_id',
                            5:'title',
                            6:'release_year',
                            7:'bechdel_rating',
                            11:'language',
                            13:'popularity',
                            14:'vote_average',
                            15:'vote_count',
                            16:'overview'
                            },
                   inplace=True)
    df.drop(columns=[4, 8, 9, 10, 12], inplace=True)
    df.fillna(0, inplace=True)
    df.replace('none', np.nan, inplace=True)
    return df

def NoScripts():
    warnings.filterwarnings("ignore")
    conn = psycopg2.connect(dbname='bechdel_test', user='postgres', password='guest')
    cur = conn.cursor()

    cur.execute(
        'SELECT b.imdb_id, b.title, t.overview, b.rating FROM bechdel_ratings b  JOIN tmdb_data  t ON t.imdb_id = b.imdb_id;')
    data = pd.DataFrame(cur.fetchall())
    df = data.copy()
    cur.close()
    conn.close()

    return df.rename(columns={0: 'imdb_id',
                              1: 'title',
                              2: 'overview',
                              3: 'bechdel_rating'}
                     )

