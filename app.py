from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3
import MySQLdb as mdb
from psycopg2.extensions import AsIs

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
        return render_template('homepageauthor.html')
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
                return render_template('homepageauthor.html')
            else:
                return render_template('homepagereviewer.html')
        elif username == 'admin' and password == 'admin242':
            return render_template('homepageadmin.html')
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    authorid = 11
    msg = ''
    if request.method == 'POST':
        print('here')
        fname = request.form['firstname']
        print(fname)
        mname = request.form['middleinit']
        print(mname)
        lname = request.form['lname']
        print(lname)
        affil = request.form['affil']
        print(affil)
        department = request.form['dpmt']
        print(department)
        address = request.form['address']
        print(address)
        city = request.form['city']
        print(city)
        state = request.form['state']
        print(state)
        zipCode = request.form['zip']
        print(zipCode)
        phone = request.form['phone']
        print(phone)
        email = request.form['email']
        print(email)
        usertype = request.form['usertype']
        print(usertype)
        password = request.form['password']
        print(password)
        confpass = request.form['confirmpass']
        print(confpass)

        if password != confpass:
            msg = 'Passwords do not match'
            return render_template('newaccount.html', msg=msg)

        cur.execute('INSERT INTO author (AuthorID, FirstName, MiddleInitial, LastName, Affiliation, Department, Address, City, State, ZipCode, PhoneNumber, EmailAddress, Password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (authorid, fname, mname, lname, affil, department, address, city, state, zipCode, phone, email, password ))
        db.commit()

        msg = 'Account successfully created!'
        return render_template('login.html', msg=msg)

    return render_template('newaccount.html')

@app.route('/authorreg')
def authorreg():
    return render_template('authorreg.html')

@app.route('/reviewreg',  methods=['GET', 'POST'])
def reviewreg():
    if request.method == "POST":
        topic = request.form['topic']
        reviewer_id = cur.execute("SELECT ReviewerID FROM reviewer WHERE EmailAddress = %s", [session['id']])
        statement1 = 'Update reviewer SET %s = ' 
        statement2 = '1 WHERE ReviewerID = %s'
        fix1 = statement1 % topic
        fix2 = statement2 % reviewer_id
        input = fix1 + fix2
        print(input)
        cur.execute(input)
        db.commit()
        print(cur._last_executed)
        print(cur.execute('Select Firstname from reviewer where ReviewerID = 1'))
        msg = 'Successfully Registered!'
        return render_template('registerforreview.html', msg = msg)
        pass
    return render_template('registerforreview.html')

@app.route('/reports')
def scorebreakdown():
    return render_template('scorereport.html')

@app.route('/uploadreview')
def uploadreview():
    return render_template('uploadreview.html')

@app.route('/viewpaper')
def viewpaper():
    reviewer_id = cur.execute("SELECT ReviewerID FROM reviewer WHERE EmailAddress = %s", [session['id']])
    print(reviewer_id)
    cur.execute('select paper.PaperID, Title, FilenameOriginal from paper natural join review where ReviewerID = %s', [reviewer_id])
    papers = cur.fetchall()
    print(papers)

    return render_template('viewpapers.html', papers = papers)


#manages uploading papers
@app.route('/uploadpaper', methods=['GET', 'POST'])
def uploadpaper():
    print('in function upload')

    PaperID = cur.execute("SELECT COUNT(*) FROM paper")
    PaperID = cur.fetchone()[0]
    PaperID += 1
    print(PaperID)

    author_id = cur.execute("SELECT AuthorID FROM author WHERE EmailAddress = %s", [session['id']])
    print(author_id)

    if request.method == 'POST':
        print('in request method')
        title = request.form['title']
        print(title)
        file = request.files['paperfile']
        print(file)
        print('past file')
        topic = request.form['topic']
        print(topic)

        print(title)
        print(file.filename)
        print(topic)

        if not title:
            flash('Title is required!')
        else:
            #statement1= "INSERT INTO paper (PaperID, AuthorID, Title, FilenameOriginal, %s) VALUES (%s, %s, %s, %s, 1)"
            statement1= "INSERT INTO paper (PaperID, AuthorID, Title, FilenameOriginal, Active, %s) "
            values1 = (topic)
            new = statement1 % values1
            print(new)
            statement2=  "VALUES (%s, %s, %s, %s, 1, 1)"
            values = (PaperID, author_id, title, file.filename)
            input = new + statement2
            print(input)
            cur.execute(input, values)
            #cur.execute('INSERT INTO paper (PaperID, AuthorID, Title, FilenameOriginal, %s) VALUES (%s, %s, %s, %s, 1)', (AsIs(topic), PaperID, author_id, title, file.filename))
            print(cur._last_executed)
            print('query executed')
            db.commit()
            return render_template('homepageauthor.html')
  
    return render_template('uploadpaper.html')

@app.route('/usermaintenance')
def usermaintenance():
    cur.execute('SELECT * FROM author')
    users = cur.fetchall()
    for user in users:
        print(user)
    return render_template('usermaintenance.html', users = users)

@app.route('/authoraccount', methods=['GET', 'POST'])
def authoraccount():
    print('in author account')
    msg = ''

    if request.method == 'POST':
        author_id = cur.execute("SELECT AuthorID FROM author WHERE EmailAddress = %s", [session['id']])
        print('in request method')
        to_update = request.form['to_update']
        print(to_update)
        new_val = request.form['newval']
        print(new_val)
        password = request.form['password']
        print(password)

        valid = cur.execute('SELECT * FROM author WHERE Password = %s', [password])

        if valid:
            print('valid')
            statement1 = 'Update author SET %s = ' 
            statement2 = '%s WHERE AuthorID = %s'
            value = to_update
            inputs = (new_val, author_id)
            new = statement1 % value
            print(new)
            input = new + statement2
            print(input)
            cur.execute(input, inputs)
            db.commit()
            print(cur._last_executed)
            print(cur.execute('Select Firstname from author where AuthorID = 1'))
            msg = 'Account change successful!'
            return render_template('authoraccount.html', msg = msg)

    return render_template('authoraccount.html')

@app.route('/revieweraccount')
def revieweraccount():
    print('in reviewer account')
    msg = ''

    if request.method == 'POST':
        reviewer_id = cur.execute("SELECT ReviewerID FROM reviewer WHERE EmailAddress = %s", [session['id']])
        print('in request method')
        to_update = request.form['to_update']
        print(to_update)
        new_val = request.form['newval']
        print(new_val)
        password = request.form['password']
        print(password)

        valid = cur.execute('SELECT * FROM reviewer WHERE Password = %s', [password])

        if valid:
            print('valid')
            statement1 = 'Update reviewer SET %s = ' 
            statement2 = '%s WHERE ReviewerID = %s'
            value = to_update
            inputs = (new_val, reviewer_id)
            new = statement1 % value
            print(new)
            input = new + statement2
            print(input)
            cur.execute(input, inputs)
            db.commit()
            print(cur._last_executed)
            print(cur.execute('Select Firstname from reviewer where ReviewerID = 1'))
            msg = 'Account change successful!'
            return render_template('revieweraccount.html', msg = msg)
    return render_template('revieweraccount.html')

@app.route('/retrieve', methods=['GET', 'POST'])
def retrieve():
    msg = ''
    if request.method == "POST":
        email = request.form['email']
        print(email)
        zipcode = request.form['zipcode']
        print(zipcode)

        cur.execute('SELECT Password FROM author WHERE EmailAddress = %s and ZipCode = %s UNION SELECT Password FROM reviewer WHERE EmailAddress = %s and ZipCode = %s', (email, zipcode, email, zipcode))
        valid = cur.fetchone()


        if valid:
            print('Valid')
            password = valid[0]
            print(password)
            msg = 'Your password is ' + password
            flash(msg)
            return render_template('getpassword.html', msg = msg)

    return render_template('getpassword.html')

@app.route('/distribute', methods=['GET', 'POST'])
def distribute():
    msg = ''
    if request.method == "POST":
        topic = request.form['topic']
        print(topic)

        statement1 = "SELECT ReviewerID, FirstName, LastName, EmailAddress, ReviewsAcknowledged  from reviewer Where Active = 1 AND ReviewsAcknowledged < 3 AND" 
        statement2 =" %s = 1"
        fixed = statement2 % topic
        print(fixed)
        input = statement1 + fixed
        print(input)

        print(cur.execute(input))
        reviewers = cur.fetchall()

        if len(reviewers) > 0:
            print('in if statement')
            msg = "Here is a list of qualified reviewers:"
            print(msg)
            print(reviewers)
            return render_template("reviewpaper.html")


    return render_template("reviewpaper.html")
