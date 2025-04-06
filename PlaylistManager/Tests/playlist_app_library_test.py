from playlist import Playlist
import pytest
import json
import playlist_app_library
from tracklist import Tracklist
from song import Song

def test_add_one_song():
    songs = []
    playlist = Playlist("Test", songs)
    assert playlist.count_songs() == 0
    playlist_app_library.add_one_song(playlist, "Bed Chem", "Sabrina Carpenter")
    assert playlist.count_songs() == 1
    playlist_app_library.add_one_song(playlist, "Bang!", "AJR")
    assert playlist.count_songs() == 2
    with pytest.raises(ValueError):
        playlist_app_library.add_one_song(playlist, "", "")
    with pytest.raises(ValueError):
        playlist_app_library.add_one_song(playlist, "ghjg", "hjsgf")

def test_add_by_artist():
    songs = []
    playlist = Playlist("Test", songs)
    assert playlist.count_songs() == 0
    playlist_app_library.add_by_artist(playlist, "Taylor Swift", 8)
    assert playlist.count_songs() == 8
    playlist_app_library.add_by_artist(playlist, "Sabrina Carpenter", 2)
    assert playlist.count_songs() == 10
    for track in playlist.tracklist:
        print(track)
    with pytest.raises(ValueError):
        playlist_app_library.add_by_artist(playlist, "", 2)
    with pytest.raises(ValueError):
        playlist_app_library.add_by_artist(playlist, "Olivia Rodrigo", -2)
    with pytest.raises(ValueError):
        playlist_app_library.add_by_artist(playlist, "Adele", 0)

def test_add_by_keyword():
    songs = []
    playlist = Playlist("Test", songs)
    assert playlist.count_songs() == 0
    playlist_app_library.add_by_keyword(playlist, "happy", 3)
    assert playlist.count_songs() == 3
    playlist_app_library.add_by_keyword(playlist, "the", 4)
    assert playlist.count_songs() == 7
    with pytest.raises(ValueError):
        playlist_app_library.add_by_keyword(playlist, "and", -5)
    with pytest.raises(ValueError):
        playlist_app_library.add_by_keyword(playlist, "Hello", 0)

def test_search_by_genre():
    songs = []
    playlist = Playlist("Test", songs)
    assert playlist.count_songs() == 0
    playlist_app_library.add_by_artist(playlist, "Sabrina Carpenter", 2)
    pop_list1 = playlist_app_library.search_by_genre(playlist, "Pop")
    assert len(pop_list1) == 2
    playlist_app_library.add_by_artist(playlist, "Ariana Grande", 3)
    pop_list2 = playlist_app_library.search_by_genre(playlist, "Pop")
    assert len(pop_list2) == 5
    with pytest.raises(ValueError):
        playlist_app_library.search_by_genre(playlist, "")
    with pytest.raises(ValueError):
        playlist_app_library.search_by_genre(playlist, "Country")

def test_search_by_artist():
    songs = []
    playlist = Playlist("Test", songs)
    assert playlist.count_songs() == 0
    playlist_app_library.add_by_artist(playlist, "Sabrina Carpenter", 2)
    sc_list1 = playlist_app_library.search_by_artist(playlist, "Sabrina Carpenter")
    assert len(sc_list1) == 2
    playlist_app_library.add_by_artist(playlist, "Olivia Rodrigo", 3)
    playlist_app_library.add_by_artist(playlist, "Ariana Grande", 4)
    playlist_app_library.add_by_artist(playlist, "Sabrina Carpenter", 3)
    sc_list2 = playlist_app_library.search_by_artist(playlist, "Sabrina Carpenter")
    assert len(sc_list2) == 5
    or_list = playlist_app_library.search_by_artist(playlist, "Olivia Rodrigo")
    assert len(or_list) == 3
    ag_list = playlist_app_library.search_by_artist(playlist, "Ariana Grande")
    assert len(ag_list) == 4
    with pytest.raises(ValueError):
        playlist_app_library.search_by_artist(playlist, "Taylor Swift")
    with pytest.raises(ValueError):
        playlist_app_library.search_by_artist(playlist, "")

def test_search_one():
    songs = []
    playlist = Playlist("Test", songs)
    playlist_app_library.add_one_song(playlist, "Bed Chem", "Sabrina Carpenter")
    playlist_app_library.add_one_song(playlist, "Bang!", "AJR")
    bc_position = playlist_app_library.search_one(playlist, "Bed Chem", "Sabrina Carpenter")
    assert bc_position == 1
    playlist_app_library.add_one_song(playlist, "Bed Chem", "Sabrina Carpenter")
    bc_pos = playlist_app_library.search_one(playlist, "Bed Chem", "Sabrina Carpenter")
    assert bc_pos == 1
    bang_pos = playlist_app_library.search_one(playlist, "Bang!", "AJR")
    assert bang_pos == 2
    with pytest.raises(ValueError):
        playlist_app_library.search_one(playlist, "Espresso", "Sabrina Carpenter")
    with pytest.raises(ValueError):
        playlist_app_library.search_one(playlist, "", "")
    with pytest.raises(ValueError):
        playlist_app_library.search_one(playlist, "Bed Chem", "")
    with pytest.raises(ValueError):
        playlist_app_library.search_one(playlist, "", "AJR")

def test_sort_by_artist():
    songs = []
    playlist = Playlist("Test", songs)
    with pytest.raises(ValueError):
        playlist_app_library.sort_by_artist(playlist)
    playlist_app_library.add_one_song(playlist, "Bed Chem", "Sabrina Carpenter")
    playlist_app_library.add_one_song(playlist, "Bang!", "AJR")
    playlist_app_library.add_one_song(playlist, "Espresso", "Sabrina Carpenter")
    playlist_app_library.add_one_song(playlist, "Stitches", "Shawn Mendes")
    playlist_app_library.add_one_song(playlist, "pov", "Ariana Grande")
    expected = ["Bang!", "pov", "Bed Chem", "Espresso", "Stitches"]
    playlist_app_library.sort_by_artist(playlist)
    tracks = playlist.tracklist
    actual = []
    for track in tracks:
        actual.append(track.title)
    assert expected == actual

def test_sort_by_genre():
    '''unsure of genres so print all first to see genre and again after sort to make sure the order is correct'''
    playlist = Playlist("Test", [])
    with pytest.raises(ValueError):
        playlist_app_library.sort_by_genre(playlist)
    playlist_app_library.add_one_song(playlist, "Bed Chem", "Sabrina Carpenter")
    playlist_app_library.add_one_song(playlist, "Bang!", "AJR")
    playlist_app_library.add_one_song(playlist, "Espresso", "Sabrina Carpenter")
    playlist_app_library.add_one_song(playlist, "Piano Man", "Billy Joel")
    playlist_app_library.add_one_song(playlist, "pov", "Ariana Grande")
    playlist_app_library.add_one_song(playlist, "Speechless", "Dan + Shay")
    for song in playlist.tracklist:
        print(song)
    playlist_app_library.sort_by_genre(playlist)
    tracklist = playlist.tracklist
    for song in tracklist:
        print(song)

def test_sort_by_title():
    playlist = Playlist("Test", [])
    with pytest.raises(ValueError):
        playlist_app_library.sort_by_genre(playlist)
    playlist_app_library.add_one_song(playlist, "Bed Chem", "Sabrina Carpenter")
    playlist_app_library.add_one_song(playlist, "Bang!", "AJR")
    playlist_app_library.add_one_song(playlist, "Espresso", "Sabrina Carpenter")
    playlist_app_library.add_one_song(playlist, "Piano Man", "Billy Joel")
    playlist_app_library.add_one_song(playlist, "pov", "Ariana Grande")
    playlist_app_library.add_one_song(playlist, "Speechless", "Dan + Shay")
    playlist_app_library.add_one_song(playlist, "Karma", "Taylor Swift")
    playlist_app_library.add_one_song(playlist, "Karma", "AJR")
    expected_title = ["Bang!", "Bed Chem", "Espresso", "Karma", "Karma", "Piano Man", "pov", "Speechless"]
    expected_artist = ["AJR", "Sabrina Carpenter", "Sabrina Carpenter", "AJR", "Taylor Swift", "Billy Joel", "Ariana Grande", "Dan + Shay"]
    playlist_app_library.sort_by_title(playlist)
    tracks = playlist.tracklist
    actual_title = []
    actual_artist = []
    for track in tracks:
        actual_title.append(track.title)
        actual_artist.append(track.artist)
    assert expected_title == actual_title
    assert expected_artist == actual_artist

def test_get_genres():
    playlist = Playlist("Test", [])
    genres1 = playlist_app_library.get_genres(playlist)
    assert genres1 == []
    playlist_app_library.add_one_song(playlist, "Bed Chem", "Sabrina Carpenter")
    playlist_app_library.add_one_song(playlist, "Bang!", "AJR")
    playlist_app_library.add_one_song(playlist, "Espresso", "Sabrina Carpenter")
    playlist_app_library.add_one_song(playlist, "Piano Man", "Billy Joel")
    playlist_app_library.add_one_song(playlist, "pov", "Ariana Grande")
    playlist_app_library.add_one_song(playlist, "Speechless", "Dan + Shay")
    genres2 = playlist_app_library.get_genres(playlist)
    expected = ["Pop", "Folk-Rock", "Dance"]
    assert genres2 == expected

def test_get_artists():
    playlist = Playlist("Test", [])
    artists1 = playlist_app_library.get_artists(playlist)
    assert artists1 == []
    playlist_app_library.add_one_song(playlist, "Bed Chem", "Sabrina Carpenter")
    playlist_app_library.add_one_song(playlist, "Bang!", "AJR")
    playlist_app_library.add_one_song(playlist, "Espresso", "Sabrina Carpenter")
    playlist_app_library.add_one_song(playlist, "Piano Man", "Billy Joel")
    playlist_app_library.add_one_song(playlist, "pov", "Ariana Grande")
    playlist_app_library.add_one_song(playlist, "Speechless", "Dan + Shay")
    artists2 = playlist_app_library.get_artists(playlist)
    expected = ["Sabrina Carpenter", "AJR", "Billy Joel", "Ariana Grande", "Dan + Shay"]
    assert artists2 == expected

def test_get_songs_with_lyrics():
    playlist = Playlist("Test", [])
    artists1 = playlist_app_library.get_artists(playlist)
    assert artists1 == []
    assert playlist_app_library.get_songs_with_lyrics(playlist) == []
    playlist_app_library.add_one_song(playlist, "Bed Chem", "Sabrina Carpenter")
    playlist_app_library.add_one_song(playlist, "Bang!", "AJR")
    playlist_app_library.add_one_song(playlist, "Espresso", "Sabrina Carpenter")
    playlist_app_library.add_one_song(playlist, "Piano Man", "Billy Joel")
    playlist_app_library.add_one_song(playlist, "pov", "Ariana Grande")
    playlist_app_library.add_one_song(playlist, "Speechless", "Dan + Shay")
    has_lyrics = playlist_app_library.get_songs_with_lyrics(playlist)
    expected = ["Bed Chem", "Bang!", "Espresso", "Piano Man", "pov", "Speechless"]
    has_lyrics_titles = []
    for song in has_lyrics:
        has_lyrics_titles.append(song.title)
    assert has_lyrics_titles == expected

def test_random_lyrics():
    '''print lyrics to ensure it works'''
    playlist = Playlist("Test", [])
    artists1 = playlist_app_library.get_artists(playlist)
    assert artists1 == []
    with pytest.raises(ValueError):
        playlist_app_library.random_lyrics(playlist)
    playlist_app_library.add_one_song(playlist, "Bed Chem", "Sabrina Carpenter")
    playlist_app_library.add_one_song(playlist, "Bang!", "AJR")
    playlist_app_library.add_one_song(playlist, "Espresso", "Sabrina Carpenter")
    playlist_app_library.add_one_song(playlist, "Piano Man", "Billy Joel")
    playlist_app_library.add_one_song(playlist, "pov", "Ariana Grande")
    playlist_app_library.add_one_song(playlist, "Speechless", "Dan + Shay")
    lyrics = playlist_app_library.random_lyrics(playlist)
    print(lyrics)



