from flask import Flask, request, render_template
import psycopg2
from psycopg2 import Error
import random

# change these values according to your local machine
user = 'postgres'
password = '1234'
port = '5432'           # for Ben it's 5432, for Philip it's 5433
database = 'phase2'     # may be different for you depending on what database you are using on your local mahcine
                        # for me i had to create another database different from postgres which is default
                        # then create all the tables and insert the data
try:
    # Connect to an existing database
    connection = psycopg2.connect(user=user,
                                  password=password,
                                  host="localhost",
                                  port=port,
                                  database=database)

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")
    # Executing a SQL query
    cursor.execute("SELECT version();")
    # Fetch result
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

#make changes
def get_db_connection():
    conn = psycopg2.connect(
        user=user,
        password=password,
        host="localhost",
        port=port,
        database=database
    )
    return conn

#-----------this is the part to test if you can connect to postgresql---------------




# testing to see how well using a global user variable works
username = None
password = None

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/user-login', methods=['GET', 'POST'])
def user_login():
    global username
    global password
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s",
                    (username, password))
        user = cur.fetchone()   # user is a tuple ie (0, 'user0', 'pass0')
        username = user[1]  # 1 is the user name in the tuple
        password = user[2]  # this grabs the password within the tuple
        cur.close()
        conn.close()
        if user:
            return render_template('playlist.html', user=user)
        else:
            credential='Invalid Credentials. Try Again'
            return render_template('login.html', credential=credential)     # this will display invalid/valid credentials on the same page instead of redirecting to a new page
    else:
        return render_template('login.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        user_id = random.randint(11, 10000) # randomly generate a user_id
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("INSERT INTO users (user_id, username, password) VALUES (%s, %s, %s)",
                    (user_id, username, password))
        
        conn.commit()
        cur.close()
        conn.close()
        
        credential = 'Account created successfully. Please Enter Credentials'
        return render_template('login.html', credential=credential)
    else:
        return render_template('create_account.html')

# this is for the general use of navigating back and forth from playlist page once user has already logged in
@app.route('/playlist', methods=['GET', 'POST'])
def playlist():
    global username
    user_id = username  # Replace with the actual logged-in user's ID
    print(user_id)
    # playlist_name = request.form['playlist_name']

    # conn = get_db_connection()
    # cur = conn.cursor()

    # cur.execute("INSERT INTO playlist (user_id, playlist_name) VALUES (%s, %s) RETURNING playlist_name", (user_id, playlist_name))
    # playlist_id = cur.fetchone()[0]

    # cur.execute("SELECT * FROM playlist WHERE playlist_name = %s", (playlist_id,))
    # new_playlist = cur.fetchone()

    # conn.commit()
    # cur.close()
    # conn.close()

    return render_template('playlist.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    global username
    songs_list = ()
    
    # display all songs upon loading up the page
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM songs_list")
    songs_list = cur.fetchall()
    # print(songs_list)
    
    conn.commit()
    cur.close()
    conn.close()
    
    if request.method == 'POST':
        # get user submitted song name and playlist
        song = request.form['song']
        playlist = request.form['playlist']
        
        # now add to database specifying user, song, and playlist
        conn = get_db_connection()
        cur = conn.cursor()

        # first we want to add to the song table the song that was chosen that references the playlist name
        # randomly generate the other columns - song_id, num_listens, and album_id
        song_id = random.randint(11, 10000)
        num_listens = random.randint(1, 1000000)
        album_id = random.randint(11, 100000)
        
        cur.execute("INSERT INTO song (song_id, song_name, num_listens, album_id, playlist_name) VALUES (%s,%s,%s,%s,%s)", 
                    (song_id, song, num_listens, album_id, playlist))

        conn.commit()
        cur.close()
        conn.close()
    
    return render_template('search.html', songs_list=songs_list)

@app.route('/my_account', methods=['GET', 'POST'])
def my_account():
    global username
    global password
    return render_template('my_account.html', username=username, password=password) # render username and password upon loeading this page


if __name__ == "__main__":
    app.run(debug=True)