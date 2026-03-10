from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('beatles.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY, title TEXT UNIQUE, album TEXT, avg REAL DEFAULT 0, votes INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS ratings (id INTEGER PRIMARY KEY, song_title TEXT, rating REAL, timestamp TEXT)''')
    
    songs_data = [
        # Please Please Me (1963)
        {"title": "I Saw Her Standing There", "album": "Please Please Me"},
        {"title": "Misery", "album": "Please Please Me"},
        {"title": "Anna (Go to Him)", "album": "Please Please Me"},
        {"title": "Chains", "album": "Please Please Me"},
        {"title": "Boys", "album": "Please Please Me"},
        {"title": "Ask Me Why", "album": "Please Please Me"},
        {"title": "Please Please Me", "album": "Please Please Me"},
        {"title": "Love Me Do", "album": "Please Please Me"},
        {"title": "P.S. I Love You", "album": "Please Please Me"},
        {"title": "Baby It's You", "album": "Please Please Me"},
        {"title": "Do You Want to Know a Secret", "album": "Please Please Me"},
        {"title": "A Taste of Honey", "album": "Please Please Me"},
        {"title": "There's a Place", "album": "Please Please Me"},
        {"title": "Twist and Shout", "album": "Please Please Me"},
        
        # With the Beatles (1963)
        {"title": "It Won't Be Long", "album": "With the Beatles"},
        {"title": "All I've Got to Do", "album": "With the Beatles"},
        {"title": "All My Loving", "album": "With the Beatles"},
        {"title": "Don't Bother Me", "album": "With the Beatles"},
        {"title": "Little Child", "album": "With the Beatles"},
        {"title": "Till There Was You", "album": "With the Beatles"},
        {"title": "Please Mr. Postman", "album": "With the Beatles"},
        {"title": "Roll Over Beethoven", "album": "With the Beatles"},
        {"title": "Hold Me Tight", "album": "With the Beatles"},
        {"title": "You Really Got a Hold on Me", "album": "With the Beatles"},
        {"title": "I Wanna Be Your Man", "album": "With the Beatles"},
        {"title": "Devil in Her Heart", "album": "With the Beatles"},
        {"title": "Not a Second Time", "album": "With the Beatles"},
        {"title": "Money (That's What I Want)", "album": "With the Beatles"},
        
        # A Hard Day's Night (1964)
        {"title": "A Hard Day's Night", "album": "A Hard Day's Night"},
        {"title": "I Should Have Known Better", "album": "A Hard Day's Night"},
        {"title": "If I Fell", "album": "A Hard Day's Night"},
        {"title": "I'm Happy Just to Dance with You", "album": "A Hard Day's Night"},
        {"title": "And I Love Her", "album": "A Hard Day's Night"},
        {"title": "Tell Me Why", "album": "A Hard Day's Night"},
        {"title": "Can't Buy Me Love", "album": "A Hard Day's Night"},
        {"title": "Any Time at All", "album": "A Hard Day's Night"},
        {"title": "I'll Cry Instead", "album": "A Hard Day's Night"},
        {"title": "Things We Said Today", "album": "A Hard Day's Night"},
        {"title": "When I Get Home", "album": "A Hard Day's Night"},
        {"title": "You Can't Do That", "album": "A Hard Day's Night"},
        {"title": "I'll Be Back", "album": "A Hard Day's Night"},
        
        # Beatles for Sale (1964)
        {"title": "No Reply", "album": "Beatles for Sale"},
        {"title": "I'm a Loser", "album": "Beatles for Sale"},
        {"title": "Baby's in Black", "album": "Beatles for Sale"},
        {"title": "I'll Follow the Sun", "album": "Beatles for Sale"},
        {"title": "Mr. Moonlight", "album": "Beatles for Sale"},
        {"title": "Kansas City/Hey-Hey-Hey-Hey!", "album": "Beatles for Sale"},
        {"title": "Eight Days a Week", "album": "Beatles for Sale"},
        {"title": "Words of Love", "album": "Beatles for Sale"},
        {"title": "Honey Don't", "album": "Beatles for Sale"},
        {"title": "Every Little Thing", "album": "Beatles for Sale"},
        {"title": "I Don't Want to Spoil the Party", "album": "Beatles for Sale"},
        {"title": "What You're Doing", "album": "Beatles for Sale"},
        {"title": "Everybody's Trying to Be My Baby", "album": "Beatles for Sale"},
        
        # Help! (1965)
        {"title": "Help!", "album": "Help!"},
        {"title": "The Night Before", "album": "Help!"},
        {"title": "You've Got to Hide Your Love Away", "album": "Help!"},
        {"title": "I Need You", "album": "Help!"},
        {"title": "Another Girl", "album": "Help!"},
        {"title": "You're Going to Lose That Girl", "album": "Help!"},
        {"title": "Ticket to Ride", "album": "Help!"},
        {"title": "Act Naturally", "album": "Help!"},
        {"title": "It's Only Love", "album": "Help!"},
        {"title": "You Like Me Too Much", "album": "Help!"},
        {"title": "Tell Me What You See", "album": "Help!"},
        {"title": "I've Just Seen a Face", "album": "Help!"},
        {"title": "Dizzy Miss Lizzy", "album": "Help!"},
        
        # Rubber Soul (1965)
        {"title": "Drive My Car", "album": "Rubber Soul"},
        {"title": "Norwegian Wood (This Bird Has Flown)", "album": "Rubber Soul"},
        {"title": "You Won't See Me", "album": "Rubber Soul"},
        {"title": "Nowhere Man", "album": "Rubber Soul"},
        {"title": "Think for Yourself", "album": "Rubber Soul"},
        {"title": "The Word", "album": "Rubber Soul"},
        {"title": "Michelle", "album": "Rubber Soul"},
        {"title": "What Goes On", "album": "Rubber Soul"},
        {"title": "Girl", "album": "Rubber Soul"},
        {"title": "I'm Looking Through You", "album": "Rubber Soul"},
        {"title": "In My Life", "album": "Rubber Soul"},
        {"title": "Wait", "album": "Rubber Soul"},
        {"title": "If I Needed Someone", "album": "Rubber Soul"},
        {"title": "Run for Your Life", "album": "Rubber Soul"},
        
        # Revolver (1966)
        {"title": "Taxman", "album": "Revolver"},
        {"title": "Eleanor Rigby", "album": "Revolver"},
        {"title": "I'm Only Sleeping", "album": "Revolver"},
        {"title": "Love You To", "album": "Revolver"},
        {"title": "Here, There and Everywhere", "album": "Revolver"},
        {"title": "Yellow Submarine", "album": "Revolver"},
        {"title": "She Said She Said", "album": "Revolver"},
        {"title": "Good Day Sunshine", "album": "Revolver"},
        {"title": "And Your Bird Can Sing", "album": "Revolver"},
        {"title": "For No One", "album": "Revolver"},
        {"title": "Doctor Robert", "album": "Revolver"},
        {"title": "I Want to Tell You", "album": "Revolver"},
        {"title": "Got to Get You into My Life", "album": "Revolver"},
        {"title": "Tomorrow Never Knows", "album": "Revolver"},
        
        # Sgt. Pepper's Lonely Hearts Club Band (1967)
        {"title": "Sgt. Pepper's Lonely Hearts Club Band", "album": "Sgt. Pepper's Lonely Hearts Club Band"},
        {"title": "With a Little Help from My Friends", "album": "Sgt. Pepper's Lonely Hearts Club Band"},
        {"title": "Lucy in the Sky with Diamonds", "album": "Sgt. Pepper's Lonely Hearts Club Band"},
        {"title": "Getting Better", "album": "Sgt. Pepper's Lonely Hearts Club Band"},
        {"title": "Fixing a Hole", "album": "Sgt. Pepper's Lonely Hearts Club Band"},
        {"title": "She's Leaving Home", "album": "Sgt. Pepper's Lonely Hearts Club Band"},
        {"title": "Being for the Benefit of Mr. Kite!", "album": "Sgt. Pepper's Lonely Hearts Club Band"},
        {"title": "Within You Without You", "album": "Sgt. Pepper's Lonely Hearts Club Band"},
        {"title": "When I'm Sixty-Four", "album": "Sgt. Pepper's Lonely Hearts Club Band"},
        {"title": "Lovely Rita", "album": "Sgt. Pepper's Lonely Hearts Club Band"},
        {"title": "Good Morning Good Morning", "album": "Sgt. Pepper's Lonely Hearts Club Band"},
        {"title": "Sgt. Pepper's Lonely Hearts Club Band (Reprise)", "album": "Sgt. Pepper's Lonely Hearts Club Band"},
        {"title": "A Day in the Life", "album": "Sgt. Pepper's Lonely Hearts Club Band"},
        
        # Magical Mystery Tour (1967)
        {"title": "Magical Mystery Tour", "album": "Magical Mystery Tour"},
        {"title": "The Fool on the Hill", "album": "Magical Mystery Tour"},
        {"title": "Flying", "album": "Magical Mystery Tour"},
        {"title": "Blue Jay Way", "album": "Magical Mystery Tour"},
        {"title": "Your Mother Should Know", "album": "Magical Mystery Tour"},
        {"title": "I Am the Walrus", "album": "Magical Mystery Tour"},
        {"title": "Hello, Goodbye", "album": "Magical Mystery Tour"},
        {"title": "Strawberry Fields Forever", "album": "Magical Mystery Tour"},
        {"title": "Penny Lane", "album": "Magical Mystery Tour"},
        {"title": "Baby, You're a Rich Man", "album": "Magical Mystery Tour"},
        {"title": "All You Need Is Love", "album": "Magical Mystery Tour"},
        
        # The Beatles (White Album) (1968)
        {"title": "Back in the U.S.S.R.", "album": "The Beatles"},
        {"title": "Dear Prudence", "album": "The Beatles"},
        {"title": "Glass Onion", "album": "The Beatles"},
        {"title": "Ob-La-Di, Ob-La-Da", "album": "The Beatles"},
        {"title": "Wild Honey Pie", "album": "The Beatles"},
        {"title": "The Continuing Story of Bungalow Bill", "album": "The Beatles"},
        {"title": "While My Guitar Gently Weeps", "album": "The Beatles"},
        {"title": "Happiness Is a Warm Gun", "album": "The Beatles"},
        {"title": "Martha My Dear", "album": "The Beatles"},
        {"title": "I'm So Tired", "album": "The Beatles"},
        {"title": "Blackbird", "album": "The Beatles"},
        {"title": "Piggies", "album": "The Beatles"},
        {"title": "Rocky Raccoon", "album": "The Beatles"},
        {"title": "Don't Pass Me By", "album": "The Beatles"},
        {"title": "Why Don't We Do It in the Road?", "album": "The Beatles"},
        {"title": "I Will", "album": "The Beatles"},
        {"title": "Julia", "album": "The Beatles"},
        {"title": "Birthday", "album": "The Beatles"},
        {"title": "Yer Blues", "album": "The Beatles"},
        {"title": "Mother Nature's Son", "album": "The Beatles"},
        {"title": "Everybody's Got Something to Hide Except Me and My Monkey", "album": "The Beatles"},
        {"title": "Sexy Sadie", "album": "The Beatles"},
        {"title": "Helter Skelter", "album": "The Beatles"},
        {"title": "Long, Long, Long", "album": "The Beatles"},
        {"title": "Revolution 1", "album": "The Beatles"},
        {"title": "Honey Pie", "album": "The Beatles"},
        {"title": "Savoy Truffle", "album": "The Beatles"},
        {"title": "Cry Baby Cry", "album": "The Beatles"},
        {"title": "Revolution 9", "album": "The Beatles"},
        {"title": "Good Night", "album": "The Beatles"},
        
        # Yellow Submarine (1969)
        {"title": "Yellow Submarine", "album": "Yellow Submarine"},
        {"title": "Only a Northern Song", "album": "Yellow Submarine"},
        {"title": "All Together Now", "album": "Yellow Submarine"},
        {"title": "Hey Bulldog", "album": "Yellow Submarine"},
        {"title": "It's All Too Much", "album": "Yellow Submarine"},
        
        # Abbey Road (1969)
        {"title": "Come Together", "album": "Abbey Road"},
        {"title": "Something", "album": "Abbey Road"},
        {"title": "Maxwell's Silver Hammer", "album": "Abbey Road"},
        {"title": "Oh! Darling", "album": "Abbey Road"},
        {"title": "Octopus's Garden", "album": "Abbey Road"},
        {"title": "I Want You (She's So Heavy)", "album": "Abbey Road"},
        {"title": "Here Comes the Sun", "album": "Abbey Road"},
        {"title": "Because", "album": "Abbey Road"},
        {"title": "You Never Give Me Your Money", "album": "Abbey Road"},
        {"title": "Sun King", "album": "Abbey Road"},
        {"title": "Mean Mr. Mustard", "album": "Abbey Road"},
        {"title": "Polythene Pam", "album": "Abbey Road"},
        {"title": "She Came In Through the Bathroom Window", "album": "Abbey Road"},
        {"title": "Golden Slumbers", "album": "Abbey Road"},
        {"title": "Carry That Weight", "album": "Abbey Road"},
        {"title": "The End", "album": "Abbey Road"},
        {"title": "Her Majesty", "album": "Abbey Road"},
        
        # Let It Be (1970)
        {"title": "Two of Us", "album": "Let It Be"},
        {"title": "Dig a Pony", "album": "Let It Be"},
        {"title": "Across the Universe", "album": "Let It Be"},
        {"title": "I Me Mine", "album": "Let It Be"},
        {"title": "Dig It", "album": "Let It Be"},
        {"title": "Let It Be", "album": "Let It Be"},
        {"title": "Maggie Mae", "album": "Let It Be"},
        {"title": "The Long and Winding Road", "album": "Let It Be"},
        {"title": "For You Blue", "album": "Let It Be"},
        {"title": "Get Back", "album": "Let It Be"},
        
        # Other (non-album singles)
        {"title": "From Me to You", "album": "Other"},
        {"title": "Thank You Girl", "album": "Other"},
        {"title": "She Loves You", "album": "Other"},
        {"title": "I'll Get You", "album": "Other"},
        {"title": "I Want to Hold Your Hand", "album": "Other"},
        {"title": "This Boy", "album": "Other"},
        {"title": "I Feel Fine", "album": "Other"},
        {"title": "She's a Woman", "album": "Other"},
        {"title": "Yes It Is", "album": "Other"},
        {"title": "I'm Down", "album": "Other"},
        {"title": "Day Tripper", "album": "Other"},
        {"title": "We Can Work It Out", "album": "Other"},
        {"title": "Paperback Writer", "album": "Other"},
        {"title": "Rain", "album": "Other"},
        {"title": "Lady Madonna", "album": "Other"},
        {"title": "The Inner Light", "album": "Other"},
        {"title": "Hey Jude", "album": "Other"},
        {"title": "Revolution", "album": "Other"},
        {"title": "Don't Let Me Down", "album": "Other"},
        {"title": "The Ballad of John and Yoko", "album": "Other"},
        {"title": "Old Brown Shoe", "album": "Other"},
        {"title": "You Know My Name (Look Up the Number)", "album": "Other"}
    ]

    for song in songs_data:
        c.execute("INSERT OR IGNORE INTO songs (title, album) VALUES (?, ?)", (song["title"], song["album"]))
    conn.commit()
    conn.close()

init_db()

def recalculate_avg(song_title):
    conn = sqlite3.connect('beatles.db')
    c = conn.cursor()
    c.execute("SELECT AVG(rating), COUNT(*) FROM ratings WHERE song_title = ?", (song_title,))
    result = c.fetchone()
    avg = round(result[0], 1) if result[0] else 0.0
    votes = result[1] if result[1] else 0
    c.execute("UPDATE songs SET avg = ?, votes = ? WHERE title = ?", (avg, votes, song_title))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('beatles.db')
    c = conn.cursor()
    c.execute("SELECT title, album, avg, votes FROM songs ORDER BY avg DESC, votes DESC")
    songs = c.fetchall()
    conn.close()
    return render_template('index.html', songs=songs)

@app.route('/rate', methods=['POST'])
def rate():
    title = request.form['title']
    rating = float(request.form['rating'])
    conn = sqlite3.connect('beatles.db')
    c = conn.cursor()
    c.execute("INSERT INTO ratings (song_title, rating, timestamp) VALUES (?, ?, ?)", 
              (title, rating, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    recalculate_avg(title)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
