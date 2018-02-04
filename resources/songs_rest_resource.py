import requests
from flask_restful import reqparse, Resource

import config
from data import songs_db_wrapper


class Songs(Resource):

    def __init__(self, **kwargs):
        self.default_song_parameters = kwargs['default_song_parameters']
        self.data_arguments_parser = reqparse.RequestParser()
        self.route_data_arguments_parser = reqparse.RequestParser()
        self.request_data = {'key': kwargs['youtube_request_key'], 'part': kwargs['youtube_request_part']}
        self.songs_db = songs_db_wrapper.SongsDbWrapper(*kwargs['db_args'])
        for argument in kwargs['data_arguments_list']:
            self.data_arguments_parser.add_argument(argument)

    def get(self):
        return self.songs_db.get_songs_data()

    def post(self):
        args = self.data_arguments_parser.parse_args()
        song_id = args['song_id']
        song_name = self._get_song_name_(song_id)
        return self.songs_db.add_song(song_id, song_name)

    def _get_song_name_(self, song_id):
        self.request_data['id'] = song_id
        print self.request_data
        try:
            response_as_json = requests.get(config.youtube_api.YOUTUBE_API_URL,
                                            params=self.request_data,
                                            headers=config.youtube_api.YOUTUBE_REQUEST_HEADER).json()
            youtube_song_cell = response_as_json['items']
            youtube_song_name = youtube_song_cell[0]['snippet']['title']
            return youtube_song_name
        except Exception:
            raise
            return


