from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from resources import Songs
from resources import Song
from resources import NextSong
import config
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app)
songs_resource_kwargs = {
    'json_database_path': config.playlist.PLAYLIST_DATA_JSON_PATH,
    'default_song_parameters': config.playlist.DEFAULT_SONG_PARAMETERS,
    'youtube_request_key': config.youtube_api.YOUTUBE_REQUEST_KEY,
    'youtube_request_part': config.youtube_api.YOUTUBE_REQUEST_PART,
    'data_arguments_list': config.requests_arguments.POST_SONG_REQUEST_ARGUMENTS,
    'db_args': (config.db.DB_URL, config.db.DB_NAME, config.db.COLLECTION_NAME)
}

song_resource_kwargs = {
    'json_database_path': config.playlist.PLAYLIST_DATA_JSON_PATH,
    'data_arguments_list': config.requests_arguments.LIKE_SONG_REQUEST_ARGUMENTS,
    'db_args': (config.db.DB_URL, config.db.DB_NAME, config.db.COLLECTION_NAME)

}

next_song_resource_kwargs = {
    'json_database_path': config.playlist.PLAYLIST_DATA_JSON_PATH,
}

api.add_resource(Songs, '/songs', resource_class_kwargs=songs_resource_kwargs)
api.add_resource(Song, '/songs/<string:song_id>', resource_class_kwargs=song_resource_kwargs)
api.add_resource(NextSong, '/nextsong', resource_class_kwargs=next_song_resource_kwargs)

CORS(app)

if __name__ == '__main__':
    app.run(threaded=True, debug=True, host = 'localhost')

