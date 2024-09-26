from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    movies = db.relationship('Movie', backref='user', lazy=True)
    reviews = db.relationship('Review', back_populates='user')

class Movie(db.Model):
    __tablename__ = 'movie'
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    director_id = db.Column(db.Integer, db.ForeignKey('director.director_id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.genre_id'))
    reviews = db.relationship('Review', back_populates='movie')
    director = db.relationship('Director', backref='directed_movies')
    genre = db.relationship('Genre', backref='genre_movies')

class Review(db.Model):
    __tablename__ = 'review'
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    user = db.relationship('User', back_populates='reviews')
    movie = db.relationship('Movie', back_populates='reviews')

class Director(db.Model):
    __tablename__ = 'director'
    director_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date)
    # Changed backref name to 'directed_movies' to avoid conflict

class Genre(db.Model):
    __tablename__ = 'genre'
    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    # Changed backref name to 'genre_movies' to avoid conflict

