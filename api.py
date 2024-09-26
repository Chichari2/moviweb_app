
from flask import Blueprint, jsonify, request
from models import db, User, Movie

api = Blueprint('api', __name__)

@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.user_id, 'name': user.name} for user in users])

@api.route('/users/<int:user_id>/movies', methods=['GET'])
def get_user_movies(user_id):
    user = User.query.get_or_404(user_id)
    movies = Movie.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': movie.movie_id,
        'title': movie.title,
        'year': movie.year,
        'rating': movie.rating
    } for movie in movies])

@api.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    data = request.get_json()
    title = data['title']
    year = data.get('year')
    rating = data.get('rating')

    new_movie = Movie(title=title, year=year, rating=rating, user_id=user_id)
    db.session.add(new_movie)
    db.session.commit()
    return jsonify({'id': new_movie.movie_id}), 201
