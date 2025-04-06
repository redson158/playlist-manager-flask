import unittest
import json
import requests

from song import Song

class TestSong(unittest.TestCase):

    def test_load_in_from_api(self):
        api_key = "*********************"
        url= "https://api.musixmatch.com/ws/1.1/track.search?q_artist=taylor%20swift&apikey=" + api_key
        response = requests.get(url)
        if response.status_code == 200:
            songs_json = response.json()
            with open('test_data.json', "w") as song_file:
                json.dump(songs_json, song_file, indent=4)
        with open("test_data.json", "r") as song_file:
            all_songs = json.load(song_file)
        song_list = all_songs["message"]["body"]["track_list"]
        print(len(song_list))
        song1_json = song_list[0]["track"]
        song1 = Song(song1_json)
        print(song1)

        last_song_json = song_list[len(song_list) - 1]["track"]
        last_song = Song(last_song_json)
        print(last_song)

    def test_set_lyrics(self):
        with open("test_data.json", "r") as song_file:
            all_songs = json.load(song_file)
        song_list = all_songs["message"]["body"]["track_list"]
        test_song = Song(song_list[0]["track"])
        self.assertTrue(test_song.lyrics is None)
        test_song.set_lyrics()
        self.assertFalse(test_song.lyrics is None)

        test_song2 = Song(song_list[5]["track"])
        self.assertTrue(test_song2.lyrics is None)
        test_song2.set_lyrics()
        self.assertFalse(test_song2.lyrics is None)

    def test_contains(self):
        with open("test_data.json", "r") as song_file:
            all_songs = json.load(song_file)
        song_list = all_songs["message"]["body"]["track_list"]
        test_song = Song(song_list[0]["track"])
        self.assertTrue(test_song.contains("Karaoke"))
        self.assertTrue(test_song.contains("All"))
        self.assertFalse(test_song.contains("blue"))

        test_song2 = Song(song_list[5]["track"])
        test_song2.set_lyrics()
        self.assertTrue(test_song2.contains("Sparks"))
        self.assertTrue(test_song2.contains("Commentary"))
        self.assertFalse(test_song2.contains("good"))

    def test_has_lyrics(self):
        with open("test_data.json", "r") as song_file:
            all_songs = json.load(song_file)
        song_list = all_songs["message"]["body"]["track_list"]
        test_song = Song(song_list[0])
        self.assertFalse(test_song.has_lyrics())
        test_song2 = Song(song_list[7])
        self.assertTrue(test_song2.has_lyrics())

    def test_get_lyrics(self):
        with open("test_data.json", "r") as song_file:
            all_songs = json.load(song_file)
        song_list = all_songs["message"]["body"]["track_list"]
        test_song = Song(song_list[0]["track"])
        with self.assertRaises(ValueError):
            test_song.get_lyrics()
        test_song2 = Song(song_list[6]["track"])
        expected_lyrics = "This is Big Machine Radio\nAnd we're celebrating the 12 year Anniversary\nOf Taylor Swift's debut album\nAlso called, Taylor Swift\nWhich she released back in October of 2006\nWe're playing all the songs off the album\nGoing back and hearing from Taylor at that time\nAnd you know Taylor will never forget\nA fateful meeting with Scott Borchetta\nAfter she had just finished playing at The Bluebird Cafe\n...\n\n******* This Lyrics is NOT for Commercial use *******\n(1409625011357)"
        self.assertEqual(expected_lyrics, test_song2.get_lyrics().lyrics)
