from flask import Blueprint, render_template, request
import utils

genre_bp = Blueprint('genre_blueprint', __name__, template_folder='templates')


@genre_bp.route('/<genre>')
def page_movie_genre(genre):
    movies = utils.get_movies_by_genre(genre)
    return render_template("genre.html", genre=genre, movies=movies)
