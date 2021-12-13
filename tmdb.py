import requests

import json
from datetime import datetime, timedelta

import os
import sqlite3


api_key = "82dcf919a0446ad1edfb7ffdf549476f"

# genre
genre_url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=ko"
genre_res = requests.get(genre_url)
genre_data = genre_res.json()


# movie list
result = []
    
for list_id in range(1, 10000):
    url = f"https://api.themoviedb.org/3/list/{list_id}?api_key={api_key}&language=ko"
    req = requests.get(url)
    data = req.json()
    
    try:
        for item in data['items']:
            result.append(
                {
                    'adult': item['adult'],
                    'backdrop_path': item['backdrop_path'],
                    'genre_ids': item['genre_ids'][0],
                    'id': item['id'],
                    'original_language': item['original_language'], 
                    'original_title': item['original_title'],
                    'overview': item['overview'],
                    'popularity': item['popularity'],
                    'poster_path': item['poster_path'],
                    'release_date': item['release_date'],
                    'title': item['title'],
                    'vote_average': item['vote_average'],
                    'vote_count': item['vote_count']
                    }
            )
    except:
        pass



# db에 저장
DB_FILENAME = 'movie_info.db'
DB_FILEPATH = os.path.join(os.getcwd(), DB_FILENAME)


conn = sqlite3.connect(DB_FILENAME)
cur = conn.cursor()

# genre table
cur.execute("DROP TABLE IF EXISTS Genre;")
cur.execute("""CREATE TABLE Genre (
				GenreId INTEGER NOT NULL PRIMARY KEY,
				Genre NVARCHAR(160));
			""")
			
for data in genre_data['genres']:
	cur.execute("""INSERT INTO Genre (
		GenreId, Genre
		) 
		VALUES (?, ?);
		""", (data['id'], data['name']))


# movie list table
cur.execute("DROP TABLE IF EXISTS Movie;")
cur.execute("""CREATE TABLE Movie (
				Id INTEGER NOT NULL PRIMARY KEY,
				Title NVARCHAR(160),
				GenreId INTEGER,
				Original_language NVARCHAR(160),
				Overview NVARCHAR(160),
				Popularity INTEGER,
				Vote_average FLOAT,
				Vote_count INTEGER,
				Adult NVARCHAR(160),
				Release_date NVARCHAR(160),
				Backdrop_path NVARCHAR(160),
				Poster_path NVARCHAR(160),
                FOREIGN KEY(GenreId) REFERENCES Genre(GenreId)
                )
				;
			""")
			

for data in result:
	cur.execute("""INSERT OR IGNORE INTO Movie (
		Id,
		Title,
		GenreId,
		Original_language,
		Overview,
		Popularity,
		Vote_average,
		Vote_count,
		Adult,
		Release_date,
		Backdrop_path,
		Poster_path
		) 
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
		""", (data['id'], 
			data['title'],
			data['genre_ids'],
			data['original_language'],
			data['overview'],
			data['popularity'],
			data['vote_average'],
			data['vote_count'],
			data['adult'],
			data['release_date'],
			data['backdrop_path'],
			data['poster_path']
			))


conn.commit()
conn.close()