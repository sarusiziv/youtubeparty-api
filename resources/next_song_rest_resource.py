import json
from flask_restful import reqparse, abort, Api, Resource
from data import songs_db_wrapper


class NextSong(Resource):

    def __init__(self, **kwargs):
        self.json_database_path = self.json_database_path = kwargs['json_database_path']
        self.songs_db = songs_db_wrapper.SongsDbWrapper(*kwargs['db_args'])

    def get(self):
        next_song = self.songs_db.get_top_rated_song()
        self.songs_db.delete_song(next_song["SongID"])
        return next_song["SongID"]

