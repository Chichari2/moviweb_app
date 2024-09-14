from datamanager.data_manager_interface import DataManagerInterface
from models import db, User, Movie


class SQLiteDataManager(DataManagerInterface):

  def __init__(self, db_file):
    self.db_file = db_file

  def list_all_users(self):
    return User.query.all()

  def get_user_movies(self, user_id):
    return Movie.query.filter_by(user_id=user_id).all()

  def add_movie(self, user_id, name, director, year, rating):
    new_movie = Movie(title=name, year=year, rating=rating, user_id=user_id)
    db.session.add(new_movie)
    db.session.commit()

  def delete_movie(self, movie_id):
    movie = Movie.query.get(movie_id)
    if movie:
      db.session.delete(movie)
      db.session.commit()
