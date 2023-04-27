from flask import Flask
from flask import render_template
from flask import request, url_for, flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = '14b6c6e2d3bd51c9cb52dd98800eb5faeeaa89321a019535'
# We add a secret key so that we can keep track of the session.
# Meaning we can navigate through the website, without losing the information
# we have added (e.g. registered new users)

users = {
    'vlad': 'vlad12345',
    'admin': 'admin'
}


@app.route('/')
def index():
    return render_template('index.html', users=users)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        return do_the_login()
    else:
        return show_the_login_form()


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        return do_the_register()
    else:
        return show_the_register()


def show_the_login_form():
    return render_template('login-form.html')


def do_the_login():
    user = request.form['username']
    password = request.form['password']
    print(user)
    print(password)

    if not user:
        flash("Username is required")
    elif not password:
        flash("Password is required")
    else:
        # if the form is valid, show the home page
        if user in users and (users[user] == password):
            return render_template('home.html')
        else:
            flash("Invalid Username or Password")
        # make sure to practice redirects. We can redirect the user from the
        # Register page, when they successfully add a new user to index.html
        # to show the updated user list
    return render_template('login-form.html')


def show_the_register():
    return render_template('register-form.html')


def do_the_register():
    user = request.form['username']
    password = request.form['password']
    password_confirm = request.form['password-confirm']
    if not user:
        flash("Username is required")
    elif not password:
        flash("Password is required")
    elif not password_confirm:
        flash("Please confirm the password")
    elif not (password == password_confirm):
        flash("Passwords do not match")
    elif user in users:
        flash("Username already used")
    else:
        users[user] = password
        return redirect(url_for('index'))
        # how does url_for work? Does it return the url for a file?
        # what is the difference between using redirect vs render_template here?
        # ANSWER. url returns the actual page created previously,
        # whereas render makes a whole new web page, loosing everything!
        # Or maybe, I just have to pass the arguments all over again?
        # Yeah that is it! If I render again, I would have to pass all arguments
        # all over again. I dont need that with url_for.
    return render_template('register-form.html')
