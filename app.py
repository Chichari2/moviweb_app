from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User, Movie, Director, Genre
from api import api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviweb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def home():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/user/<int:user_id>')
def user_movies(user_id):
    user = User.query.get_or_404(user_id)
    user_movies = Movie.query.filter_by(user_id=user_id).all()
    return render_template('movies.html', movies=user_movies, user=user)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('list_users'))
    return render_template('add_user.html')

@app.route('/add_movie/<int:user_id>', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        title = request.form['title']
        director_name = request.form['director']
        genre_name = request.form['genre']
        year = request.form['year']
        rating = request.form['rating']

        director = Director.query.filter_by(name=director_name).first()
        if not director:
            director = Director(name=director_name)
            db.session.add(director)

        genre = Genre.query.filter_by(name=genre_name).first()
        if not genre:
            genre = Genre(name=genre_name)
            db.session.add(genre)

        db.session.commit()

        new_movie = Movie(title=title, year=year, rating=rating, director=director, genre=genre, user_id=user_id)
        db.session.add(new_movie)
        db.session.commit()

        return redirect(url_for('user_movies', user_id=user_id))
    return render_template('add_movie.html', user_id=user_id)

@app.route('/update_movie/<int:user_id>/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    movie = Movie.query.get_or_404(movie_id)  # Получаем фильм по ID
    if request.method == 'POST':
        movie.title = request.form['title']
        movie.year = request.form['year']
        movie.rating = request.form['rating']
        db.session.commit()  # Сохраняем изменения в базе данных
        return redirect(url_for('user_movies', user_id=user_id))
    return render_template('update_movie.html', movie=movie, user_id=user_id)

@app.route('/delete_movie/<int:user_id>/<int:movie_id>')
def delete_movie(user_id, movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('user_movies', user_id=user_id))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
