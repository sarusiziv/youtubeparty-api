from flask_restful import reqparse, Resource

from data import songs_db_wrapper


class Song(Resource):

    def __init__(self, **kwargs):

        self.json_database_path = self.json_database_path = kwargs['json_database_path']
        self.data_arguments_parser = reqparse.RequestParser()
        self.songs_db = songs_db_wrapper.SongsDbWrapper(*kwargs['db_args'])
        for argument in kwargs['data_arguments_list']:
            self.data_arguments_parser.add_argument(argument)

    def get(self, song_id):
        return self.songs_db.get_song(song_id)

    def put(self, song_id):
        args = self.data_arguments_parser.parse_args()
        if args['like_endpoint'] == "true":
            return self.like_song(song_id, args['user_id'])
        elif args['like_endpoint'] == "false":
            return self.dislike_song(song_id, args['user_id'])

    def like_song(self, song_id, user_id):
        song_obj = self.songs_db.get_song(song_id, user_id)
        if user_id not in song_obj["LikesUsers"]:
            song_obj["LikesUsers"].append(user_id)
            self.songs_db.update_song(song_id, song_obj)
        return song_obj

    def dislike_song(self, song_id, user_id):
        song_obj = self.songs_db.get_song(song_id, user_id)
        if user_id not in song_obj["DislikesUsers"]:
            song_obj["DislikesUsers"].append(user_id)
            print song_obj
            self.songs_db.update_song(song_id, song_obj)
        return song_obj


