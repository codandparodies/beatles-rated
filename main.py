from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('beatles.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY, title TEXT UNIQUE, album TEXT, avg REAL DEFAULT 0, votes INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS ratings (id INTEGER PRIMARY KEY, song_title TEXT, rating REAL, timestamp TEXT)''')
    
    # === PASTE YOUR 213 SONGS HERE ===
    songs_data = [
        # ←←← Open your old beatles-rater.html file
        # Search for "let songs = ["
        # Copy everything from that line down to the final "];"
        # Paste it here (replace this comment)
        {"title": "I Saw Her Standing There", "album": "Please Please Me"},
        {"title": "Misery", "album": "Please Please Me"}
        # ... keep going until you have all songs + "Other" ...
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
