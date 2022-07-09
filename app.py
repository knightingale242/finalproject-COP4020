from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import MySQLdb as mdb

DBNAME="cpms"  # database name
#DBPORT=3306      # database port
DBHOST="localhost"  # database host
DBUSER="root"  # database user
DBPASS="root"  # database password

db= mdb.connect(DBHOST, DBUSER, DBPASS, DBNAME)
cur = db.cursor()

app = Flask(__name__)
app.secret_key = 'software engineering summer 2022'

print("hello world")

@app.route('/')
def home():
     # Check if user is loggedin
    if 'loggedin' in session:
   
        # User is loggedin show them the home page
        return render_template('homepage.html')
    # User is not loggedin redirect to login page
    print('new session')
    return redirect(url_for('login'))

'''''
@app.route('/')
def home():
    return render_template('newaccount.html')
'''''


@app.route('/login', methods=['GET', 'POST'])
def login():
    print('in login page')
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        print(username, password)
        # Check if account exists using MySQL
        cur.execute('SELECT emailAddress, password FROM reviewer WHERE emailAddress= %s AND Password = %s UNION SELECT emailAddress, password FROM author WHERE emailAddress= %s AND Password = %s', (username, password, username, password))
        # Fetch one record and return result
        account = cur.fetchone()

        print(account)
   
    # If account exists in accounts table in out database
        if account:
# Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = username
            # Redirect to home page
            #return 'Logged in successfully!'
            print('it worked')
            cur.execute('SELECT * FROM author WHERE emailAddress = %s', [username])
            account = cur.fetchone()

            if account:
                return render_template('homepage.html')
            else:
                return render_template('homepagereviewer.html')
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
            print('unsuccessful')
    
    return render_template('login.html', msg=msg)

@app.route('/scorebreakdown')
def reports():
    return render_template('scorebreakdown.html')

@app.route('/welcome')
def welcome():
    return render_template('homepage.html')

@app.route('/register')
def register():
    '''''
    if request.method == 'POST':
        fname = request.form['fname']
        mname = request.form['fname']
        lname = request.form['fname']
        affil = request.form['fname']
        department = request.form['fname']
        address = request.form['fname']
        city = request.form['fname']
        state = request.form['fname']
        zipCode = request.form['fname']
        phone = request.form['fname']
        emailadd = request.form['fname']
'''
    return render_template('newaccount.html')

@app.route('/authorreg')
def authorreg():
    return render_template('authorreg.html')

@app.route('/reviewreg')
def reviewreg():
    return render_template('registerforreview.html')

@app.route('/reports')
def scorebreakdown():
    return render_template('scorereport.html')

@app.route('/uploadreview')
def uploadreview():
    return render_template('uploadreview.html')

@app.route('/reviewpaper')
def reviewpaper():
    return render_template('reviewpaper.html')
