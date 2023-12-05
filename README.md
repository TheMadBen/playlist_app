# Playlist Application
Built using Python, Flask, HTML/CSS, PostgreSQL<br>
Flask provides the ability to locally host our web application using HTML/CSS and Python<br>
All of the data that is shown and stored is done by using PostgreSQL as our database where we establish a local connection to it<br><br>
User can login using existing login information or create an account to login<br>
Will have the ability to create playlists with a name of their choosing and add songs to playlists that they own and show it<br>

# Setup
pip install flask psycopg2<br><br>

Must be able to establish a local connection with PostgreSQL to run the code. Download PostgreSQL [here](https://www.postgresql.org/download/)<br>
Make sure the version 13 or greater and have pgAdmin4 installed as well.<br>
When you setup pgAdmin4, keep the user as postgres and port 5432 which should be default. Make the password for postgres user 1234 for the sake of not having to change the code.<br>
Once that is done, create a new database called 'phase2' by right clicking on the server name which should be PostgreSQL '[version number]'<br>
Make sure that you are on the phase2 database and not postgre database that's create by default. You are creating a new database so you don't have to change the code.<br>
Select the Query Tool located near the top left between 'Object Explorer' and 'Dashboard'.<br>
Copy and paste the sql found [here](https://github.com/TheMadBen/playlist_app/blob/main/sql_queries.txt) and run it. This should create all the table and data insertion necessary.<br><br>

With all dependencies and PostgreSQL setup, you should be able to run the code as a flask appliction using 'py -m flask run'<br><br>

# Walkthrough
will be added later once i get all the screenshots done
