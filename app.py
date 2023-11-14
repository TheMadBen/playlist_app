from flask import Flask, request, render_template

app = Flask(__name__, template_folder='templates')

# this is the first page that we see
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/account')  # this is create account page
def account():
    return render_template('account.html')

@app.route('/user-login')
# this is for the form action where the user enters their login info and clicks 'Login'
def user_login():
    return render_template('playlist.html')

@app.route('/playlist')
# this is for the general use of navigating back and forth from playlist page once user has already logged in
def playlist():
    return render_template('playlist.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/account-created')
# if user creates account, it will redirect back to login page
def account_created():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)