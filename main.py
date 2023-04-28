from flask import Flask, render_template, request, url_for, flash, \
    redirect, Response
from flask_mysqldb import MySQL
from markupsafe import escape
from typing import Union

app = Flask(__name__)
app.config['SECRET_KEY'] = '14b6c6e2d3bd51c9cb52dd98800eb5faeeaa89321a019535'
# We add a secret key so that we can keep track of the session.
# Meaning we can navigate through the website, without losing the information
# we have added (e.g. registered new users)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'first_flask'

mysql = MySQL(app)


@app.route('/')
def index() -> str:
    """Main page"""
    cursor = mysql.connection.cursor()
    # this command only selects, it does not evaluate to anything meaningful
    cursor.execute('''SELECT username, password FROM users''')
    # this thing returns a tuple of tuples
    users = cursor.fetchall()
    cursor.close()

    mysql.connection.commit()

    return render_template('index.html', users=users)


@app.route("/login", methods=['GET', 'POST'])
def login() -> str:
    """Login page"""
    if request.method == "POST":
        return do_the_login()
    else:
        return show_the_login_form()


@app.route("/register", methods=['GET', 'POST'])
def register() -> Union[str, Response]:
    """Registration page"""
    if request.method == "POST":
        return do_the_register()
    else:
        return show_the_register()

# I should probably add a route for the homepage and redirect there
# when a login is successful. I could make custom home pages using
# information about the specific user form the database combined with
# Jinja template.


def show_the_login_form() -> str:
    """
    Render the login form
    """
    return render_template('login-form.html')


def do_the_login() -> str:
    """
    Check the username and password in the database,
    show home-page if the credentials are valid.
    """
    this_user = escape(request.form['username'])
    password = escape(request.form['password'])

    # get the tuple of users
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT username, password FROM users''')
    users = cursor.fetchall()

    cursor.close()

    if not this_user:
        flash("Username is required")
    elif not password:
        flash("Password is required")
    else:
        # if the form is valid, show the home page
        for user in users:
            if user[0] == this_user and user[1] == password:
                return render_template('home.html', user=this_user)
        # if no matches found, give an error
        flash("Invalid Username or Password")

    return render_template('login-form.html')


def show_the_register() -> str:
    """
    Render the register form
    """
    return render_template('register-form.html')


def do_the_register() -> Union[str, Response]:
    """
    Validate the register form. Append the new validated user to the database.
    """
    user = escape(request.form['username'])
    password = escape(request.form['password'])
    password_confirm = escape(request.form['password-confirm'])

    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT username FROM users''')

    users = cursor.fetchall()

    if not user:
        flash("Username is required")
    elif not password:
        flash("Password is required")
    elif not password_confirm:
        flash("Please confirm the password")
    elif not (password == password_confirm):
        flash("Passwords do not match")
    # have to compare user as a tuple, I probably wanna add docstring and
    # typing to my functions at this point
    elif (user,) in users:
        flash("Username already used")
    else:
        # append the new user to the database
        cursor.execute('''INSERT INTO users VALUES (%s,%s,%s,%s)''', (user, password, '', 0))
        # make sure to save changes
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('index'))
        # how does url_for work? Does it return the url for a file?
    return render_template('register-form.html')
