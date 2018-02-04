from pymongo import MongoClient
import json
from bson.json_util import dumps
import requests
import config


class SongsDbWrapper:
    def __init__(self, db_url, db_name=None, songs_collection_name=None):
        self.db_url = db_url
        self.db_name = db_name
        self.client = MongoClient(db_url)
        self.db = None
        self.connect_to_db(db_name)
        self.collection = self.set_songs_collection(songs_collection_name)
        self.songs_collection_name = songs_collection_name

    def connect_to_db(self, db_name):
        self.db_name = db_name
        self.db = self.client[self.db_name]

    def set_songs_collection(self, songs_collection_name):
        return self.db[songs_collection_name]

    def get_songs_data(self):
        songs_list = []
        songs = self.collection.find({})
        for song in songs:
            songs_list.append(song)
        return json.loads(dumps(songs_list))

    def get_song(self, song_id):
        song = self.collection.find({'SongID': song_id})[0]
        return json.loads(dumps(song))

    def add_song(self, song_path_id, song_name):
        song_object = {"SongID": song_path_id, "LikesUsers": [], "DislikesUsers": [], "Name": song_name}
        self.collection.insert_one(song_object)
        return json.loads(dumps(song_object))

    def update_song(self, song_path_id, updated_object):
        self.collection.update_one({'SongID': song_path_id}, {"$set": updated_object}, upsert=False)
        return json.loads(dumps(updated_object))

    def delete_song(self, song_path_id):
        self.collection.delete_one({'SongID': song_path_id})

    def get_top_rated_song(self):
        songs = self.get_songs_data()
        top_rated_song_id = songs[0]["SongID"]
        top_rated_points = len(songs[0]["LikesUsers"]) - len(songs[0]["DislikesUsers"])
        for song in songs:
            points_count = len(song["LikesUsers"]) - len(song["DislikesUsers"])
            if points_count > top_rated_points:
                top_rated_song_id = song["SongID"]
                top_rated_points = points_count
        return self.get_song(top_rated_song_id)


if __name__ == '__main__':
    songs_db = SongsDbWrapper('mongodb+srv://admin:SecPass1@cluster0-qpidy.mongodb.net/test',
                              "youtubeparty", "songs")

    print songs_db.get_top_rated_song()
