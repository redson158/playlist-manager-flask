import requests
import json
from song import Song

class Tracklist:

    def __init__(self):
        self.songs = []

    def add_song(self, song):
        '''allows to more easily make playlists with various artists/genres'''
        self.songs.append(song)

    def add_list_of_songs(self, songlist):
        '''adds list of song objects to tracklist'''
        for song in songlist:
            self.songs.append(song)

    def add_song_by_title(self, title, artist):
        '''uses title to make a call to api and create new song object'''
        api_key = "*****************"
        url = "https://api.musixmatch.com/ws/1.1/track.search?q_track=" + title + "&q_artist=" + artist +"&apikey=" + api_key
        response = requests.get(url)
        if response.status_code == 200:
            song_json = response.json()
            if len(song_json["message"]["body"]["track_list"]) > 0:
                song_parts = song_json["message"]["body"]["track_list"][0]["track"]
                new_song = Song(song_parts)
                if new_song.artist == artist:
                    self.songs.append(new_song)
                else:
                    raise ValueError("API Error")
            else:
                raise ValueError("Song Not Found")
        else:
            raise ValueError("Invalid Input")

    def add_songs_by_artist(self, artist, length):
        '''uses artist and desired number of songs to make a call to the api and create new song objects'''
        if length < 1:
            raise ValueError("Cannot Add Less Than 1 Song")
        api_key = "****************"
        url = "https://api.musixmatch.com/ws/1.1/track.search?q_artist=" + artist + "&page_size=" + str(length) +"&apikey=" + api_key
        response = requests.get(url)
        if response.status_code == 200:
            songs_json = response.json()
            song_list = songs_json["message"]["body"]["track_list"]
            for song_data in song_list:
                song_info = song_data["track"]
                new_song = Song(song_info)
                if new_song.artist == artist:
                    self.songs.append(new_song)
                else:
                    raise ValueError("API Error")
        else:
            raise ValueError("Invalid Input")

    def add_songs_by_keyword(self, keyword, length):
        '''uses keyword and desired number of songs to call api and create new song objects'''
        if length < 1:
            raise ValueError("Cannot Add Less Than One Song")
        api_key = "*****************"
        url = "https://api.musixmatch.com/ws/1.1/track.search?q=" + keyword + "&page_size=" + str(length) + "&apikey=" + api_key
        response = requests.get(url)
        if response.status_code == 200:
            songs_json = response.json()
            song_list = songs_json["message"]["body"]["track_list"]
            for song_data in song_list:
                song_info = song_data["track"]
                new_song = Song(song_info)
                self.songs.append(new_song)
        else:
            raise ValueError("Invalid Keyword")

    def get_songs(self):
        '''returns list of songs in tracklist'''
        return self.songs

    def print_list(self):
        '''returns tracklist as list of title strings'''
        list_of_str = []
        for song in self.songs:
            list_of_str.append(song.title)
        return list_of_str