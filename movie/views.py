from flask import Blueprint, render_template, request
import utils

movie_bp = Blueprint('movie_blueprint', __name__, template_folder='templates')


@movie_bp.route('/<title>')
def page_movie_title(title):
    movie = utils.get_movie_by_title(title)
    return render_template("title.html", movie=movie)

@movie_bp.route('/<first_year>/to/<second_year>')
def page_movie_year_interval(first_year, second_year):
    movies = utils.get_movies_by_year_interval(first_year, second_year)
    return render_template("movies_interval.html", first_year=first_year, second_year=second_year, movies=movies)
