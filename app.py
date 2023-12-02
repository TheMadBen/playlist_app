from flask import Flask, request, render_template
import psycopg2
from psycopg2 import Error
import random

user = 'postgres'
password = '1234'
port = '5432'           # for Ben it's 5432, for Philip it's 5433
database = 'phase2'     # may be different for you depending on what database you are using on your local mahcine

try:
    # Connect to an existing database
    connection = psycopg2.connect(user="postgres",
                                  password="1234",
                                  host="localhost",
                                  port="5432",
                                  database="phase2")

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
        user="postgres",
        password="1234",
        host="localhost",
        port="5432",
        database="phase2"
    )
    return conn

#-----------this is the part to test if you can connect to postgresql---------------




# testing to see how well using a global user variable works
user = None

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/user-login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s",
                    (username, password))
        user = cur.fetchone()   # user is a tuple ie (0, 'user0', 'pass0')
        # print(user)
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
    user_id = 0  # Replace with the actual logged-in user's ID
    # print(user_id)
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


@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/my_account', methods=['GET', 'POST'])
def my_account():

    return render_template('my_account.html')


if __name__ == "__main__":
    app.run(debug=True)