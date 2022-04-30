import sqlite3
import json
import re
from operator import itemgetter


def get_movie_by_title(title):
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()
        search_query = f'%{title}%'
        sql_query = """
                SELECT title, country, release_year, listed_in, description
                FROM netflix
                WHERE title
                LIKE ?
                ORDER BY release_year DESC
                LIMIT 1
        """
        cursor.execute(sql_query, (search_query,))
        result = cursor.fetchall()
        if not result:
            return None
        else:
            entry = result[0]

        result_dict = {
            "title": entry[0],
            "country": entry[1],
            "release_year": entry[2],
            "genre": entry[3],
            "description": entry[4]
        }

        return result_dict


def get_movies_by_year_interval(start_year, end_year):
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()
        sql_query = """
                SELECT title, release_year
                FROM netflix
                WHERE release_year >= ? AND release_year <= ?
                ORDER BY release_year DESC
                LIMIT 100
        """
        cursor.execute(sql_query, (start_year, end_year,))
        result = []
        for entry in cursor.fetchall():
            result.append({'title': entry[0], 'release_year': entry[1]})
        return result


def get_movies_by_rating(rating):
    search_query = ''
    for rating_mark in rating.split(','):
        search_query += f'^{rating_mark}$|'
    with sqlite3.connect('netflix.db') as connection:
        connection.create_function("REGEXP", 2, regexp)
        cursor = connection.cursor()
        sql_query = """
                SELECT title, rating, description
                FROM netflix
                WHERE rating REGEXP ?
                ORDER BY release_year DESC
                LIMIT 100
                """
        cursor.execute(sql_query, (search_query[:-1],))
        result = []
        for entry in cursor.fetchall():
            result.append({'title': entry[0], 'rating': entry[1], 'description': entry[2]})
        return result


def get_movies_by_genre(genre):
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()
        search_query = f'%{genre}%'
        sql_query = """
                SELECT title, description
                FROM netflix
                WHERE listed_in LIKE ?
                ORDER BY release_year
                LIMIT 10
                """
        cursor.execute(sql_query, (search_query,))
        result = cursor.fetchall()

        result_list = []
        for movie in result:
            result_list.append({'title': movie[0], 'description': movie[1]})

        return result_list


def get_actors_by_actors_pair(first_actor, second_actor):
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()
        search_query1 = f'%{first_actor}%'
        search_query2 = f'%{second_actor}%'
        sql_query = """
                SELECT "cast"
                FROM netflix
                WHERE "cast" LIKE ? AND "cast" LIKE ?
                ORDER BY release_year
                LIMIT 10
                """
        cursor.execute(sql_query, (search_query1, search_query2,))

        actors_played_with_pair = {}

        for cast_tupl in cursor.fetchall():
            actors_list = cast_tupl[0].split(', ')
            for actor in actors_list:
                if actor != first_actor and actor != second_actor:
                    if actor in actors_played_with_pair:
                        actors_played_with_pair[actor] += 1
                    else:
                        actors_played_with_pair[actor] = 1
        result_list = []
        for actor, value in actors_played_with_pair.items():
            if value > 2:
                result_list.append(actor)
        return result_list


def get_movies_list_json(type, year, genre):
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()
        search_query = f'%{genre}%'
        sql_query = """
                SELECT title, description
                FROM netflix
                WHERE type = ? AND release_year = ? AND listed_in LIKE ?
                ORDER BY release_year
                LIMIT 100
        """
        cursor.execute(sql_query, (type, year, search_query,))
        result = cursor.fetchall()
        return json.dumps(list(result))


def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None


# get_movies_list_json('Movie', '2011', 'Comedy')
