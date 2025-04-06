import requests
import json
from lyrics import Lyrics

class Song:

    def __init__(self, song_json):
        self.title = song_json["track_name"]
        self.artist = song_json["artist_name"]
        genre_list = song_json["primary_genres"]["music_genre_list"]
        self.genre = genre_list[0]["music_genre"]["music_genre_name"] if genre_list else None
        self.id = song_json["track_id"]
        self.lyrics = None
        if self.genre is None:
            self.genre = "Unknown"

    def set_lyrics(self):
        '''uses track id to call api to get lyrics for that song; creates new lyrics object and store in song'''
        api_key = "*********************"
        url = "https://api.musixmatch.com/ws/1.1/track.lyrics.get?track_id=" + str(self.id) + "&apikey=" + api_key
        response = requests.get(url)
        if response.status_code == 200:
            lyrics_json = response.json()
            if lyrics_json["message"]["body"]:
                lyric_list = lyrics_json["message"]["body"]["lyrics"]["lyrics_body"]
                self.lyrics = Lyrics(self.title, lyric_list)
            else:
                raise ValueError("Lyrics Unavailable")
        else:
            raise ValueError("Failed to retrieve data from Musixmatch API")

    def get_lyrics(self):
        '''returns lyrics if available, raises ValueError otherwise'''
        if self.has_lyrics():
            return self.lyrics
        else:
            raise ValueError("Lyrics Unavailable")

    def has_lyrics(self):
        '''returns boolean, checks to see if lyrics are available'''
        try:
            self.set_lyrics()
            if self.lyrics is not None and self.lyrics.lyrics != "":
                return True
            else:
                return False
        except ValueError:
            return False

    def get_genre(self):
        return self.genre


    def contains(self, keyword):
        '''checks to see if keyword is in title or lyrics'''
        if keyword in self.title:
            return True
        elif self.lyrics is not None:
            if keyword in self.lyrics.lyrics:
                return True
            else:
                return False
        else:
            return False

    def __str__(self):
        if self.genre is not None:
            return self.title + " by " + self.artist + " is a " + self.genre + " song"
        else:
            return self.title + " by " + self.artist