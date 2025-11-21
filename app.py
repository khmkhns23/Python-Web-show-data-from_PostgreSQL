from flask import Flask, request, jsonify , render_template
from models import db, Student, Movie
import config

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# -----------------------------
# สร้างตารางใน database
# -----------------------------
with app.app_context():
    db.create_all()



@app.route('/')
def home():
    return render_template("index.html")

@app.route('/movies')
def movie_list():
    movies = Movie.query.all()
    return render_template("movies.html", movies=movies, title="Movie List")

# -----------------------------
# CREATE
# -----------------------------
@app.route('/movie', methods=['POST'])
def create_movie():
    data = request.json
    movie = Movie(
        m_name=data['m_name'],
        release_date=data['release_date'],
        genre=data['genre'],
        country=data['country']
    )
    db.session.add(movie)
    db.session.commit()
    return jsonify({"message": "Movie created", "mid": movie.mid}), 201


@app.route('/movie/<int:mid>', methods=['GET'])
def get_movie(mid):
    movie = Movie.query.get_or_404(mid)
    return jsonify(movie.to_dict())

@app.route('/movie/<int:mid>', methods=['PUT'])
def update_movie(mid):
    movie = Movie.query.get_or_404(mid)
    data = request.json

    movie.m_name = data.get("m_name", movie.m_name)
    movie.release_date = data.get("release_date", movie.release_date)
    movie.genre = data.get("genre", movie.genre)
    movie.country = data.get("country", movie.country)

    db.session.commit()
    return jsonify({"message": "Movie updated", "movie": movie.to_dict()})

@app.route('/movie/<int:mid>', methods=['DELETE'])
def delete_movie(mid):
    movie = Movie.query.get_or_404(mid)
    db.session.delete(movie)
    db.session.commit()
    return jsonify({"message": "Movie deleted"})

# -----------------------------
# RUN
# -----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

