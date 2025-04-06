import unittest
import json
import requests

from playlist import Playlist
from tracklist import Tracklist
from song import Song

class TestPlaylist(unittest.TestCase):

    def test_playlist_creation(self):
        with open("test_data.json", "r") as song_file:
            all_songs = json.load(song_file)
        song_list = all_songs["message"]["body"]["track_list"]
        test_playlist = Playlist("Test Playlist", song_list)
        print(test_playlist)

    def test_count_songs(self):
        with open("test_data.json", "r") as song_file:
            all_songs = json.load(song_file)
        song_list = all_songs["message"]["body"]["track_list"]
        test_playlist = Playlist("Test Playlist", song_list)
        self.assertEqual(10, test_playlist.count_songs())

    def test_shorten_playlist(self):
        with open("test_data.json", "r") as song_file:
            all_songs = json.load(song_file)
        song_list = all_songs["message"]["body"]["track_list"]
        test_playlist = Playlist("Test Playlist", song_list)
        shorter1 = test_playlist.shorten_playlist(5)
        self.assertEqual(5, shorter1.count_songs())
        shorter2 = test_playlist.shorten_playlist(8)
        self.assertEqual(8, shorter2.count_songs())
        with self.assertRaises(ValueError):
            test_playlist.shorten_playlist(15)
        with self.assertRaises(ValueError):
            test_playlist.shorten_playlist(-3)

    def test_playlist_containing(self):
        with open("test_data.json", "r") as song_file:
            all_songs = json.load(song_file)
        song_list = all_songs["message"]["body"]["track_list"]
        test_playlist = Playlist("Test Playlist", song_list)
        contains1 = test_playlist.playlist_containing("SuperStar")
        self.assertEqual(1, contains1.count_songs())
        with self.assertRaises(ValueError):
            test_playlist.playlist_containing("Supercalifragilisticexpialidocious")
        contains3 = test_playlist.playlist_containing("with")
        self.assertEqual(2, contains3.count_songs())

    def test_playlist_by_genre(self):
        with open("../../172-project02-oopforanapi-redson158/test/test_data.json", "r") as song_file:
            all_songs = json.load(song_file)
        song_list = all_songs["message"]["body"]["track_list"]
        test_playlist = Playlist("Test Playlist", song_list)
        genre1 = test_playlist.playlist_by_genre("Contemporary Country")
        self.assertEqual(5, genre1.count_songs())
        genre2 = test_playlist.playlist_by_genre("Pop")
        self.assertEqual(1, genre2.count_songs())
        genre3 = test_playlist.playlist_by_genre("Rock")
        self.assertEqual(0, genre3.count_songs())

    def test_playlist_by_artist(self):
        with open("test_data.json", "r") as song_file:
            all_songs = json.load(song_file)
        song_list = all_songs["message"]["body"]["track_list"]
        test_playlist = Playlist("Test Playlist", song_list)
        artist1 = test_playlist.playlist_by_artist("Taylor Swift")
        self.assertEqual(10, artist1.count_songs())
        with self.assertRaises(ValueError):
            test_playlist.playlist_by_artist("Olivia Rodrigo")


    def test_count_songs_by_artist(self):
        with open("test_data.json", "r") as song_file:
            all_songs = json.load(song_file)
        song_list = all_songs["message"]["body"]["track_list"]
        test_playlist = Playlist("Test Playlist", song_list)
        self.assertEqual(10, test_playlist.count_songs_by_artist("Taylor Swift"))
        self.assertEqual(0, test_playlist.count_songs_by_artist("AJR"))

    def test_find_artist_with_most_songs(self):
        with open("test_data.json", "r") as song_file:
            all_songs = json.load(song_file)
        song_list = all_songs["message"]["body"]["track_list"]
        test_playlist = Playlist("Test Playlist", song_list)
        expected1 = "Taylor Swift"
        self.assertEqual(expected1, test_playlist.find_artist_with_most_songs())

    def test_create_playlist_from_songlist(self):
        song_list = Tracklist()
        song_list.add_song_by_title("Bang!", "AJR")
        song_list.add_song_by_title("Trustfall", "P!nk")
        song_list.add_songs_by_artist("Taylor Swift", 5)
        song_list.add_songs_by_keyword("love", 2)
        track_list = song_list.get_songs()
        test_playlist = Playlist("Test Playlist", track_list)
        self.assertEqual(9, test_playlist.count_songs())

    def test_set_songlist(self):
        with open("test_data.json", "r") as song_file:
            all_songs = json.load(song_file)
        song_list = all_songs["message"]["body"]["track_list"]
        test_playlist = Playlist("Test Playlist", song_list)
        song_list = Tracklist()
        song_list.add_song_by_title("Bang!", "AJR")
        song_list.add_song_by_title("Trustfall", "P!nk")
        song_list.add_songs_by_artist("Taylor Swift", 5)
        song_list.add_songs_by_keyword("love", 2)
        track_list = song_list.get_songs()
        test_playlist.set_tracklist(song_list)
        self.assertEqual(track_list, test_playlist.tracklist)

    def test_add_song(self):
        with open("../../172-project02-oopforanapi-redson158/test/test_data.json", "r") as song_file:
            all_songs = json.load(song_file)
        song_list = all_songs["message"]["body"]["track_list"]
        test_playlist = Playlist("Test Playlist", song_list)
        song1 = Song(song_list[0]["track"])
        test_playlist.add_song(song1)
        self.assertEqual(11, test_playlist.count_songs())

    def test_add_list_of_songs(self):
        with open("test_data.json", "r") as song_file:
            all_songs = json.load(song_file)
        song_list = all_songs["message"]["body"]["track_list"]
        test_playlist = Playlist("Test Playlist", song_list)
        song_list = Tracklist()
        song_list.add_song_by_title("Bang!", "AJR")
        song_list.add_song_by_title("Trustfall", "P!nk")
        song_list.add_songs_by_artist("Taylor Swift", 5)
        song_list.add_songs_by_keyword("love", 2)
        test_playlist.add_list_of_songs(song_list.songs)
        self.assertEqual(19, test_playlist.count_songs())
