from random import randint

from flask import Flask, request
from playlist import Playlist
from song import Song
import playlist_app_library
from tracklist import Tracklist

app = Flask(__name__)
songs = []
playlist = Playlist("Example Playlist", songs)

@app.route('/')
def home():
    welcome_message = """
     <html><body>
         <h2>Welcome to the Playlist Editor</h2>   
     </body></html>
    """
    tracklist = playlist.tracklist
    if len(tracklist) > 0:
        current_playlist = playlist.name + ": <br>"
        for i in range(len(tracklist)):
            song = tracklist[i]
            current_playlist += ("Track " + str(i + 1) + ": " + song.title + " by " + song.artist) + "<br>"
    else:
        current_playlist = "No Songs in Playlist"
    rename_playlist_form = """
            <form action = "/renameplaylist" method="post">
                <input type='text' name='Name'>
                <input type='submit' value='Rename Playlist'>
            </form>
        """
    add_songs_form = """
            <form action = "/addsongs" method="post">
                <input type='submit' value='Add Songs'>
            </form>
        """
    remove_song_form = """
            <form action = "/removesong" method="post">
                <input type='text' name='track_num'>
                <input type='submit' value='Remove Song'>
            </form>
        """
    clear_songs_form = """
            <form action = "/clearsongs" method="post">
                <input type='submit' value='Clear Songs'>
            </form>
        """
    search_playlist_form = """
            <form action = "/searchplaylist" method="post">
                <input type='submit' value='Search Playlist'>
            </form>
        """
    sort_playlist_form = """
            <form action = "/sortplaylist" method="post">
                <input type='submit' value='Sort Playlist'>
            </form>
        """
    view_stats_form = """
            <form action = "/viewstats" method="post">
                <input type='submit' value='View Stats'>
            </form>
        """
    view_lyrics_form = """
            <form action = "/viewlyrics" method="post">
                <input type='submit' value='View Lyrics'>
            </form>
        """
    quiz_form = """
            <form action = "/quiz" method="post">
                <input type='submit' value='Take Quiz'>
            </form>
        """
    return welcome_message + current_playlist + rename_playlist_form + add_songs_form + sort_playlist_form + search_playlist_form + remove_song_form + view_stats_form + view_lyrics_form + quiz_form + clear_songs_form


@app.route("/addsongs", methods=["POST"])
def add_menu():
    add_choices_message = """
         <html><body>
             <h2>Choose How to Add</h2>   
         </body></html>
        """
    choice_form = """
        <form action = "/addmethod" method="post">
            <h2>Enter Title, Artist, or Keyword</h2>
            <input type='text' name='Method'>
            <input type='submit' value='Submit'>
        </form>
    """
    return add_choices_message + choice_form

@app.route("/addmethod", methods=["POST"])
def add_songs():
    method = request.form.get("Method", "")
    if method == "Title" or method == "title":
        form = """
            <form action = "/addbytitle" method="post">
                <h2>Enter Song Title:</h2>
                <input type='text' name='Title'><br>
                <h2>Enter Artist Name:</h2>
                <input type='text' name='Artist'>
                <input type='submit' value='Add Song'>
            </form>
        """
    elif method == "artist" or method == "Artist":
        form = """
            <form action = "/addbyartist" method="post">
                <h2>Enter Artist Name:</h2>
                <input type='text' name='Artist'>
                <h2>Enter Number of Songs to be Added:</h2>
                <input type='text' name='Length'>
                <input type='submit' value='Add Songs'>
            </form>
        """
    elif method == "Keyword" or method == "keyword":
        form = """
            <form action = "/addbykeyword" method="post">
                <h2>Enter Keyword:</h2>
                <input type='text' name='Keyword'>
                <h2>Enter Number of Songs to be Added:</h2>
                <input type='text' name='Length'>
                <input type='submit' value='Add Songs'>
            </form>
        """
    else:
        return "Invalid Choice" + "<br><br><a href='/'> Back to Home </a>"
    return form


@app.route("/addbytitle", methods=["POST"])
def add_one():
    title = request.form.get("Title", "")
    artist = request.form.get("Artist", "")
    if title != "" and artist != "":
        try:
            playlist_app_library.add_one_song(playlist, title, artist)
            message = "Song Successfully Added"
        except ValueError:
            message = "Song Not Found"
    else:
        message = "Invalid Title or Artist"
    return message + "<br><br><a href='/'> Back to Home </a>"

@app.route("/addbyartist", methods=["POST"])
def add_by_artist():
    artist = request.form.get("Artist", "")
    length = request.form.get("Length", "")
    if artist != "" and length != "":
        try:
            num_add = int(length)
            if num_add < 1:
                message = "Cannot Add Less Than 1 Song"
            else:
                playlist_app_library.add_by_artist(playlist, artist, num_add)
                message = "Songs Successfully Added"
        except ValueError:
            message = "Artist Not Found"
    else:
        message = "Invalid Input"
    return message + "<br><br><a href='/'> Back to Home </a>"

@app.route("/addbykeyword", methods=["POST"])
def add_by_keyword():
    keyword = request.form.get("Keyword", "")
    length = request.form.get("Length", "")
    if keyword != "" and length != "":
        try:
            num_add = int(length)
            if num_add < 1:
                message = "Cannot Add Less Than 1 Song"
            else:
                playlist_app_library.add_by_keyword(playlist, keyword, num_add)
                message = "Songs Successfully Added"
        except ValueError:
            message = "Keyword not Found"
    else:
        message = "Invalid Input"
    return message + "<br><br><a href='/'> Back to Home </a>"

@app.route("/renameplaylist", methods=["POST"])
def rename_confirmation():
    name = request.form.get("Name", "")
    if name != "":
        playlist.set_playlist_name(name)
        message = "Playlist Successfully Renamed"
    else:
        message = "Invalid Input"
    return message + "<br><br><a href='/'> Back to Home </a>"

@app.route("/removesong", methods=["POST"])
def deletion_confirmation():
    track_num = request.form.get("track_num", "")
    try:
        index = int(track_num) - 1
        if index < 0 or index >= len(playlist.tracklist):
            raise IndexError
        playlist.tracklist.pop(index)
        message = "Track " + track_num + " Successfully Deleted"
    except ValueError:
        message = "Invalid Track Number"
    except IndexError:
        message = "Track Not Found"
    return message + "<br><br><a href='/'> Back to Home </a>"

@app.route("/clearsongs", methods=["POST"])
def clear_all_confirmation():
    playlist.tracklist.clear()
    message = "All Songs Cleared"
    return message + "<br><br><a href='/'> Back to Home </a>"

@app.route("/searchplaylist", methods=["POST"])
def choose_search_method():
    add_choices_message = """
             <html><body>
                 <h2>Choose How to Search</h2>   
             </body></html>
            """
    choice_form = """
            <form action = "/searchmethod" method="post">
                <h2>Enter Title, Artist, or Genre</h2>
                <input type='text' name='Method'>
                <input type='submit' value='Submit'>
            </form>
        """
    return add_choices_message + choice_form

@app.route("/searchmethod", methods=["POST"])
def search_playlist():
    method = request.form.get("Method", "")
    if method == "Title" or method == "title":
        form = """
            <form action = "/searchbytitle" method="post">
                <h2>Enter Song Title:</h2>
                <input type='text' name='Title'><br>
                <h2>Enter Artist Name:</h2>
                <input type='text' name='Artist'>
                <input type='submit' value='Search Playlist'>
            </form>
        """
    elif method == "artist" or method == "Artist":
        form = """
            <form action = "/searchbyartist" method="post">
                <h2>Enter Artist Name:</h2>
                <input type='text' name='Artist'>
                <input type='submit' value='Search Playlist'>
            </form>
        """
    elif method == "Genre" or method == "genre":
        form = """
            <form action = "/searchbygenre" method="post">
                <h2>Enter Genre:</h2>
                <input type='text' name='Genre'>
                <input type='submit' value='Search Playlist'>
            </form>
        """
    else:
        return "Invalid Choice" + "<br><br><a href='/'> Back to Home </a>"
    return form

@app.route("/searchbytitle", methods=["POST"])
def search_by_title():
    title = request.form.get("Title", "")
    artist = request.form.get("Artist", "")
    if title != "" and artist != "":
        try:
            index = playlist_app_library.search_one(playlist, title, artist)
            message = title + " by " + artist + " is Track " + str(index) + " in the playlist"
        except ValueError:
            message = "Song Not Found"
    else:
        message = "Invalid Title or Artist"
    return message + "<br><br><a href='/'> Back to Home </a>"

@app.route("/searchbyartist", methods=["POST"])
def search_by_artist():
    artist = request.form.get("Artist", "")
    if artist != "":
        try:
            by_artist = playlist_app_library.search_by_artist(playlist, artist)
            message = "Tracks by " + artist + ": <br>"
            for i in range(len(by_artist)):
                song = by_artist[i]
                message += song.title + "<br>"
        except ValueError:
            message = "Artist Not Found"
    else:
        message = "Invalid Input"
    return message + "<br><br><a href='/'> Back to Home </a>"

@app.route("/searchbygenre", methods=["POST"])
def search_by_genre():
    genre = request.form.get("Genre", "")
    if genre != "":
        try:
            of_genre = playlist_app_library.search_by_genre(playlist, genre)
            message = genre + " Tracks: <br>"
            for i in range(len(of_genre)):
                song = of_genre[i]
                message += song.title + " by " + song.artist + "<br>"
        except ValueError:
            message = "Genre not Found"
    else:
        message = "Invalid Input"
    return message + "<br><br><a href='/'> Back to Home </a>"

@app.route("/sortplaylist", methods=["POST"])
def choose_sort_method():
    add_choices_message = """
             <html><body>
                 <h2>Choose How to Sort</h2>   
             </body></html>
            """
    choice_form = """
            <form action = "/sortmethod" method="post">
                <h2>Enter Title, Artist, or Genre</h2>
                <input type='text' name='Method'>
                <input type='submit' value='Submit'>
            </form>
        """
    return add_choices_message + choice_form

@app.route("/sortmethod", methods=["POST"])
def sort_playlist():
    method = request.form.get("Method", "")
    if method == "Title" or method == "title":
        form = """
            <form action = "/sortbytitle" method="post">
                <h2>Sort by Title</h2>
                <input type='submit' value='Sort Playlist'>
            </form>
        """
    elif method == "artist" or method == "Artist":
        form = """
            <form action = "/sortbyartist" method="post">
                <h2>Sort by Artist</h2>
                <input type='submit' value='Sort Playlist'>
            </form>
        """
    elif method == "Genre" or method == "genre":
        form = """
            <form action = "/sortbygenre" method="post">
                <h2>Sort by Genre</h2>
                <input type='submit' value='Sort Playlist'>
            </form>
        """
    else:
        return "Invalid Choice" + "<br><br><a href='/'> Back to Home </a>"
    return form

@app.route("/sortbytitle", methods=["POST"])
def sort_by_title():
    try:
        playlist_app_library.sort_by_title(playlist)
        message = "Playlist Successfully Sorted"
    except ValueError:
        message = "No Songs in Playlist to Sort"
    return message + "<br><br><a href='/'> Back to Home </a>"

@app.route("/sortbyartist", methods=["POST"])
def sort_by_artist():
    try:
        playlist_app_library.sort_by_artist(playlist)
        message = "Playlist Successfully Sorted"
    except ValueError:
        message = "No Songs in Playlist to Sort"
    return message + "<br><br><a href='/'> Back to Home </a>"

@app.route("/sortbygenre", methods=["POST"])
def sort_by_genre():
    try:
        playlist_app_library.sort_by_genre(playlist)
        genres = playlist_app_library.get_genres(playlist)
        message = "Playlist Successfully Sorted <br> Genres Included: <br>"
        for genre in genres:
            message += genre + "<br>"
    except ValueError:
        message = "No Songs in Playlist With Genre Attribute"
    return message + "<br><br><a href='/'> Back to Home </a>"

@app.route("/viewstats", methods=["POST"])
def view_stat():
    length = playlist.count_songs()
    if length > 0:
        message = playlist.name + " is a playlist of " + str(length) + " songs <br><br>"
        genres = playlist_app_library.get_genres(playlist)
        message += "Genres Included: <br>"
        for genre in genres:
            message += genre + "<br>"
        most_artist = playlist.find_artist_with_most_songs()
        message += "<br>" + most_artist + " has the most songs in the playlist <br><br>"
        artists = playlist_app_library.get_artists(playlist)
        for artist in artists:
            song_count = playlist.count_songs_by_artist(artist)
            message += artist + ": " + str(song_count) + " songs <br>"
    else:
        message = "No Songs in Playlist"
    return message + "<br><br><a href='/'> Back to Home </a>"

@app.route("/viewlyrics", methods=["POST"])
def lyric_choices():
    lyric_choices_message = """
                 <html><body>
                     <h2>Choose What Lyrics to View</h2>   
                 </body></html>
                """
    choice_form = """
                <form action = "/viewmethod" method="post">
                    <h2>Enter Track or All</h2>
                    <input type='text' name='Method'>
                    <input type='submit' value='Submit'>
                </form>
            """
    return lyric_choices_message + choice_form

@app.route("/viewmethod", methods=["POST"])
def lyrics_method():
    method = request.form.get("Method", "")
    if method == "Track" or method == "track":
        view_one_form = """
                <form action = '/viewone' method="post">
                    <h2>Enter Song Title</h2>
                    <input type='text' name='Title'>
                    <h2>Enter Artist</h2>
                    <input type='text' name='Artist'>
                    <input type='submit' value='Get Lyrics'>
                </form>
            """
        return view_one_form
    elif method == "All" or method == "all":
        message = ""
        for track in playlist.tracklist:
            message += track.title + " by " + track.artist + "<br>"
            try:
                lyrics = track.get_lyrics()
                printable_lyrics = lyrics.print_lyrics_only()
                message += "Lyrics: " + printable_lyrics + "<br><br>"
            except ValueError:
                message += "Lyrics Unavailable <br><br>"
        return message + "<br><br><a href='/'> Back to Home </a>"
    else:
        message = "Invalid Choice"
        return message + "<br><br><a href='/'> Back to Home </a>"

@app.route("/viewone", methods=["POST"])
def display_lyrics():
    title = request.form.get("Title", "")
    artist = request.form.get("Artist", "")
    try:
        index = playlist_app_library.search_one(playlist, title, artist)
    except ValueError:
        message = "Song Not in Playlist"
        return message + "<br><br><a href='/'> Back to Home </a>"
    try:
        message = title + " by " + artist + "<br>"
        tracks = playlist.tracklist
        track = tracks[index - 1]
        lyrics = track.get_lyrics()
        printable_lyrics = lyrics.print_lyrics_only()
        message += "Lyrics: " + printable_lyrics + "<br>"
        return message + "<br><br><a href='/'> Back to Home </a>"
    except ValueError:
        message = title + " by " + artist + ": Lyrics Unavailable <br>"
        return message + "<br><br><a href='/'> Back to Home </a>"

@app.route("/quiz", methods=["POST"])
def question_one():
    if playlist.count_songs() > 0:
        message = "Welcome to the Quiz!! <br><br> Question 1: How Many Songs are in the Playlist? <br><br>"
        quiz1_form = """
                <form action = '/quizone' method="post">
                    <input type='text' name='Guess'>
                    <input type='hidden' name='num_completed' value='1'>
                    <input type= 'hidden' name='num_correct' value='0'>
                    <input type='submit' value='Submit Guess'>
                </form>
            """
        return message + quiz1_form
    else:
        message = "Must Have At Least One Song in Playlist"
        return message + "<br><br><a href='/'> Back to Home </a>"

@app.route("/quizone", methods=["POST"])
def question_two():
    guess = request.form.get("Guess", "")
    num_completed = int(request.form.get("num_completed", 0))
    num_correct = int(request.form.get("num_correct", 0))
    try:
        num = int(guess)
        if num == playlist.count_songs():
            num_correct += 1
            message = "Correct! You have " + str(num_correct) + " out of " + str(num_completed) + " questions correct. <br>"
        else:
            message = "Incorrect. You have " + str(num_correct) + " out of " + str(num_completed) + " questions correct. <br>"
    except ValueError:
        message = "Incorrect. You have " + str(num_correct) + " out of " + str(num_completed) + " questions correct. <br>"
    message += "Question 2: Which Artist Has the Most Songs in the Playlist? <br><br>"
    artists = playlist_app_library.get_artists(playlist)
    artists.sort(key=lambda artist: artist.lower())
    choices = ""
    for i in range(len(artists)):
        artist = artists[i]
        choices += "Artist" + str(i + 1) + ": " + artist + "<br>"
    quiz2_form = f"""
                <form action = '/quiztwo' method="post">
                    <h2>Enter Artist Name</h2>
                    <input type='text' name='Artist'>
                    <input type='hidden' name='num_completed' value='{num_completed + 1}'>
                    <input type='hidden' name='num_correct' value='{num_correct}'>
                    <input type='submit' value='Submit Guess'>
                </form>
            """
    return message + choices + quiz2_form

@app.route("/quiztwo", methods=["POST"])
def question_three():
    artist_guess = request.form.get("Artist", "")
    num_completed = int(request.form.get("num_completed", 0))
    num_correct = int(request.form.get("num_correct", 0))
    most_artist = playlist.find_artist_with_most_songs()
    song_count = playlist.count_songs_by_artist(most_artist)
    if artist_guess.lower() == most_artist.lower() or playlist.count_songs_by_artist(artist_guess) == song_count:
        num_correct += 1
        message = "Correct! You have " + str(num_correct) + " out of " + str(num_completed) + " questions correct. <br>"
    else:
        message = "Incorrect. You have " + str(num_correct) + " out of " + str(num_completed) + " questions correct. <br>"
    message += "Question 3: Name a Genre Included in the Playlist <Br>"
    quiz3_form = f"""
                <form action = '/quizthree' method="post">
                    <input type='text' name='Genre'>
                    <input type='hidden' name='num_completed' value='{num_completed + 1}'>
                    <input type='hidden' name='num_correct' value='{num_correct}'>
                    <input type='submit' value='Submit Guess'>
                </form>
            """
    return message + quiz3_form

@app.route("/quizthree", methods=["POST"])
def final_question():
    genre_guess = request.form.get("Genre", "")
    num_completed = int(request.form.get("num_completed", 0))
    num_correct = int(request.form.get("num_correct", 0))
    genres_covered = playlist_app_library.get_genres(playlist)
    if genre_guess in genres_covered:
        num_correct += 1
        message = "Correct! You have " + str(num_correct) + " out of " + str(num_completed) + " questions correct. <br>"
    else:
        message = "Incorrect. You have " + str(num_correct) + " out of " + str(num_completed) + " questions correct. <br>"
    has_lyrics = playlist_app_library.get_songs_with_lyrics(playlist)
    if len(has_lyrics) > 1:
        message += "Question 4: Which of these tracks are the following lyrics from? <br>"
        choices = ""
        for i in range(len(has_lyrics)):
            song = has_lyrics[i]
            choices += ("Track " + str(i + 1) + ": " + song.title + " by " + song.artist) + "<br>"
        index = randint(0, len(has_lyrics) - 1)
        song = has_lyrics[index]
        song_lyrics = song.get_lyrics()
        lyrics = song_lyrics.print_lyrics_only()
        quiz4_form = f""" 
                <form action='/quizfour' method="post"> 
                    <h2>Enter Track Number</h2> 
                    <input type='text' name='track_num'> 
                    <input type='hidden' name='num_completed' value='{num_completed + 1}'> 
                    <input type='hidden' name='num_correct' value='{num_correct}'> 
                    <input type='hidden' name='index' value='{index}'> 
                    <input type='submit' value='Submit Guess'> 
                </form> 
            """
        return message + choices + f"<p>{lyrics}</p>" + quiz4_form
    else:
        results_form = f"""
                <form action = '/quizresults' method="post">
                    <input type='hidden' name='num_completed' value='{num_completed}'>
                    <input type='hidden' name='num_correct' value='{num_correct}'>
                    <input type='submit' value='See Results'>
                </form>
            """
    return message + results_form

@app.route("/quizfour", methods=["POST"])
def check_final_question():
    track_num = int(request.form.get("track_num", ""))
    num_completed = int(request.form.get("num_completed", 0))
    num_correct = int(request.form.get("num_correct", 0))
    index = int(request.form.get("index", ""))
    if index == track_num - 1:
        num_correct += 1
        message = "Correct! You have " + str(num_correct) + " out of " + str(num_completed) + " questions correct. <br>"
    else:
        message = "Incorrect. You have " + str(num_correct) + " out of " + str(num_completed) + " questions correct. <br>"
    results_form = f"""
                    <form action = '/quizresults' method="post">
                        <input type='hidden' name='num_completed' value='{num_completed}'>
                        <input type='hidden' name='num_correct' value='{num_correct}'>
                        <input type='submit' value='See Results'>
                    </form>
                """
    return message + results_form

@app.route("/quizresults", methods=["POST"])
def quiz_results():
    num_completed = int(request.form.get("num_completed", 0))
    num_correct = int(request.form.get("num_correct", 0))
    if num_completed == num_correct or num_completed == num_correct + 1:
        message = "Congratulations!! <br> Results: You got " + str(num_correct) + " out of " + str(num_completed) + " questions correct!!<br><br>"
    elif num_correct == 0 or num_correct == 1:
        message = "Better Luck Next Time <br> Results: You got " + str(num_correct) + " out of " + str(num_completed) + " questions correct.<br><br>"
    else:
        message = "Results: You got " + str(num_correct) + " out of " + str(num_completed) + " questions correct.<br><br>"
    return message + "<br><br><a href='/'> Back to Home </a>"

if __name__ == "__main__":
    app.run(host="localhost", debug=True)

