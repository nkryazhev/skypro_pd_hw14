from flask import Blueprint, render_template
import utils

rating_bp = Blueprint('rating_blueprint', __name__, template_folder='templates')


@rating_bp.route('/children')
def page_rating_children():
    movies = utils.get_movies_by_rating('G,TV-G')
    return render_template("rating.html", rating='For children', movies=movies)


@rating_bp.route('/family')
def page_rating_family():
    movies = utils.get_movies_by_rating('G,TV-G,PG,TV-PG,PG-13')
    return render_template("rating.html", rating='For family', movies=movies)


@rating_bp.route('/adult')
def page_rating_adult():
    movies = utils.get_movies_by_rating('R,NC-17,TV-MA')
    return render_template("rating.html", rating='For adults', movies=movies)


@rating_bp.route('/<rating>')
def page_rating(rating):
    movies = utils.get_movies_by_rating(rating)
    return render_template("rating.html", rating=rating, movies=movies)
