from flask import Flask

from movie.views import movie_bp
from genre.views import genre_bp
from rating.views import rating_bp

app = Flask(__name__)

app.register_blueprint(movie_bp, url_prefix='/movie')
app.register_blueprint(genre_bp, url_prefix='/genre')
app.register_blueprint(rating_bp, url_prefix='/rating')
if __name__ == '__main__':
    app.run(debug=True)