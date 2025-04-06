from random import randint

from song import Song
from tracklist import Tracklist
from playlist import Playlist

def add_one_song(playlist, title, artist):
    '''post: adds one specific song'''
    tracklist = Tracklist()
    tracklist.add_song_by_title(title, artist)
    song = tracklist.songs[0]
    playlist.add_song(song)

def add_by_artist(playlist, artist, length):
    '''post: adds songs by specific artist'''
    tracklist = Tracklist()
    tracklist.add_songs_by_artist(artist, length)
    playlist.add_list_of_songs(tracklist.songs)


def add_by_keyword(playlist, keyword, length):
    '''post: adds songs with keyword in title or lyrics'''
    tracklist = Tracklist()
    tracklist.add_songs_by_keyword(keyword, length)
    playlist.add_list_of_songs(tracklist.songs)

def sort_by_artist(playlist):
    '''post: tracklist sorted in alphabetical order by artist, then song title'''
    tracks = playlist.tracklist
    if len(tracks) != 0:
        tracks.sort(key=lambda track: (track.artist.lower(), track.title.lower()))
    else:
        raise ValueError("No Songs in Playlist")

def sort_by_genre(playlist):
    '''post: tracklist sorted in alphabetical order by genre, then song title; skips tracks with no genre'''
    tracks = playlist.tracklist
    if len(tracks) != 0:
        tracks.sort(key=lambda song: (song.genre.lower(), song.title.lower()))
    else:
        raise ValueError("No Songs in Playlist")

def sort_by_title(playlist):
    '''post: tracklist sorted in alphabetical order by title, then artist'''
    tracks = playlist.tracklist
    if len(tracks) != 0:
        tracks.sort(key=lambda track: (track.title.lower(), track.artist.lower()))
    else:
        raise ValueError("No Songs in Playlist")

def search_by_genre(playlist, genre):
    '''returns list of songs from playlist of that genre'''
    if genre == "":
        raise ValueError("No Genre Entered")
    of_genre = []
    for song in playlist.tracklist:
        if song.genre == genre:
            of_genre.append(song)
    if len(of_genre) > 0:
        return of_genre
    else:
        raise ValueError("No Songs from Genre")

def search_by_artist(playlist, artist):
    '''returns list of songs from playlist by that artist'''
    if artist == "":
        raise ValueError("No Artist Entered")
    by_artist = []
    for song in playlist.tracklist:
        if song.artist == artist:
            by_artist.append(song)
    if len(by_artist) > 0:
        return by_artist
    else:
        raise ValueError("No Songs by Artist")

def search_one(playlist, title, artist):
    '''returns what position in the playlist the song is in'''
    if title == "" or artist == "":
        raise ValueError("Invalid Input")
    index = -1
    tracklist = playlist.tracklist
    for song in tracklist:
        if song.artist == artist and song.title == title:
            index = tracklist.index(song)
            return index + 1
    if index == -1:
        raise ValueError("Song Not in Playlist")

def get_genres(playlist):
    '''returns list of all genres in playlist'''
    genres = []
    tracks = playlist.tracklist
    for track in tracks:
        genre = track.get_genre()
        if genre is not None:
            if genre not in genres:
                genres.append(genre)
    return genres

def get_artists(playlist):
    '''returns list of all artists sorted by number of songs descending'''
    artists = []
    tracks = playlist.tracklist
    for track in tracks:
        artist = track.artist
        if artist not in artists:
            artists.append(artist)
    if len(artists) > 0:
        artists.sort(key=lambda artist: playlist.count_songs_by_artist(artist), reverse=True)
    return artists

def get_songs_with_lyrics(playlist):
    '''returns list of songs from playlist that have lyrics available'''
    has_lyrics = []
    tracks = playlist.tracklist
    for track in tracks:
        if track.has_lyrics():
            has_lyrics.append(track)
    return has_lyrics

def random_lyrics(playlist):
    '''returns lyrics from random track in playlist if any have lyrics'''
    has_lyrics = get_songs_with_lyrics(playlist)
    if len(has_lyrics) > 0:
        index = randint(0, len(has_lyrics) - 1)
        song = has_lyrics[index]
        lyrics = song.get_lyrics()
        return lyrics.print_lyrics_only()
    else:
        raise ValueError("No Songs with Lyrics Available")
