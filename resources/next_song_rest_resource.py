import json
from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify


class NextSong(Resource):

    def __init__(self, **kwargs):
        self.json_database_path = self.json_database_path = kwargs['json_database_path']

    def get(self):
        song_id = self._get_next_song_()
        self._delete_next_song_from_array_(song_id)
        self._delete_disliked_limit_()
        return song_id

    def _get_next_song_(self):
        top_liked = 0
        top_song_id = ""
        with open(self.json_database_path, "r+") as jsonFile:
            data = json.load(jsonFile)

        for song in data['songs']:
            if data['songs'][song]['likes'] >= top_liked:
                top_liked = data['songs'][song]['likes']
                top_song_id = song
        return top_song_id

    def _delete_next_song_from_array_(self, song_id):
        with open(self.json_database_path, "r+") as jsonFile:
            data = json.load(jsonFile)
        data['songs'].pop(song_id)
        with open(self.json_database_path, "w+") as jsonFile:
            json.dump(data, jsonFile)

    def _delete_disliked_limit_(self):
        disliked_limit = 3
        top_disliked_id = []

        with open(self.json_database_path, "r+") as jsonFile:
            data = json.load(jsonFile)

        for song in data['songs']:
            if data['songs'][song]['dislikes'] >= disliked_limit:
                top_disliked_id.append(song)

        for song in top_disliked_id:
            if data['songs'][song]['dislikes'] >= disliked_limit:
                data['songs'].pop(song_id)
        with open(self.json_database_path, "w+") as jsonFile:
            json.dump(data, jsonFile)

