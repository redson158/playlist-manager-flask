class Lyrics:

    def __init__(self, title, lyrics_body):
        self.title = title
        self.lyrics = lyrics_body

    def __str__(self):
        return self.title + ": " + self.lyrics

    def print_lyrics_only(self):
        '''returns lyrics body only'''
        return self.lyrics