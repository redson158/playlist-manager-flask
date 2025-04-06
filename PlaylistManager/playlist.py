from song import Song
class Playlist:

    def __init__(self, name, songs_json_or_list):
        self.name = name
        self.tracklist = []
        if len(songs_json_or_list) == 0:
            self.tracklist = []
        elif isinstance(songs_json_or_list[0], dict):
            for song_json in songs_json_or_list:
                song_info = song_json["track"]
                new_song = Song(song_info)
                self.tracklist.append(new_song)
        elif isinstance(songs_json_or_list[0], Song):
            self.tracklist = songs_json_or_list
        else:
            raise ValueError("Invalid Input")

    def set_playlist_name(self, name):
        '''post: renames playlist'''
        self.name = name

    def set_tracklist(self, tracklist):
        '''post: replaces tracklist'''
        self.tracklist = tracklist.songs

    def add_song(self, song):
        '''post: one song added to tracklist'''
        self.tracklist.append(song)

    def add_list_of_songs(self, song_list):
        '''post: list of songs added to tracklist'''
        for song in song_list:
            self.tracklist.append(song)

    def count_songs(self):
        '''returns number of songs in playlist'''
        return len(self.tracklist)

    def shorten_playlist(self, new_length):
        '''returns new playlist of desired length'''
        if new_length < 1:
            raise ValueError()
        elif new_length > len(self.tracklist):
            raise ValueError()
        else:
            new_list = []
            for i in range(new_length):
                new_list.append(self.tracklist[i])
            short_playlist = Playlist("Short and Sweet", new_list)
            return short_playlist

    def playlist_containing(self, keyword):
        '''returns new playlist of songs with keyword in title or lyrics'''
        new_list = []
        for song in self.tracklist:
            if song.contains(keyword):
                new_list.append(song)
        if len(new_list) > 0:
            name = keyword + " Playlist"
            contains_playlist = Playlist(name, new_list)
            return contains_playlist
        else:
            raise ValueError("No songs with keyword")

    def playlist_by_genre(self, genre):
        '''creates new playlist of songs only of that genre'''
        new_list = []
        for song in self.tracklist:
            if song.genre == genre:
                new_list.append(song)
        if len(new_list) > 0:
            name = genre + " Playlist"
            genre_playlist = Playlist(name, new_list)
            return genre_playlist
        else:
            raise ValueError("No Songs from Genre")

    def playlist_by_artist(self, artist):
        '''creates new playlist of songs only by one artist'''
        new_list = []
        for song in self.tracklist:
            if song.artist == artist:
                new_list.append(song)
        if len(new_list) > 0:
            name = artist + " Playlist"
            artist_playlist = Playlist(name, new_list)
            return artist_playlist
        else:
            raise ValueError("No Songs by Artist")

    def count_songs_by_artist(self, artist):
        '''return number of songs by artist in the playlist'''
        count = 0
        for song in self.tracklist:
            if song.artist == artist:
                count += 1
        return count

    def find_artist_with_most_songs(self):
        '''returns artist with most songs in playlist'''
        top_artist = None
        top_count = 0
        for song in self.tracklist:
            artist = song.artist
            song_count = self.count_songs_by_artist(artist)
            if song_count > top_count:
                top_count = song_count
                top_artist = artist
        return top_artist


    def __str__(self):
        return self.name + ": A Playlist of " + str(self.count_songs()) + " songs"
