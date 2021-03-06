from genericpath import exists
from tracemalloc import stop
from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3
import MySQLdb as mdb
from psycopg2.extensions import AsIs

from connector import PaperID

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
        cur.execute('SELECT * FROM author WHERE emailAddress = %s', [session['id']])
        account = cur.fetchone()

        if account:
            return render_template('homepageauthor.html')
        elif session['id'] == "admin":
            return render_template('homepageadmin.html')
        else:
            return render_template('homepagereviewer.html')
        # User is loggedin show them the home page
        #return render_template('homepageauthor.html')
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
            print(session['id'])
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
            session['loggedin'] = True
            session['id'] = username
            return render_template('homepageadmin.html')
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
            print('unsuccessful')
    
    return render_template('login.html', msg=msg)

@app.route('/scorebreakdown', methods=['GET', 'POST'])
def scorebreakdown():
    cur.execute("SELECT AuthorID FROM author WHERE EmailAddress = %s", [session['id']])
    author_id = cur.fetchone()

    cur.execute('select ReviewID, review.Paperid, Title, AppropriatenessOfTopic, TimelinessOfTopic, SupportiveEvidence, TechnicalQuality, ScopeOfCoverage, CitationOfPreviousWork, Originality, OrganizationOfPaper, ClarityOfMainMessage, Mechanics, SuitabilityForPresentation, PotentialInterestInTopic, OverallRating, ComfortLevelTopic, ComfortLevelAcceptability from review natural join paper where authorid = %s', [author_id[0]]) 
    papers = cur.fetchall()
    print(papers)
    for paper in papers:
        print(paper)
    return render_template('scorebreakdown.html', papers = papers)

@app.route('/authors')
def authors():
    cur.execute('SELECT AuthorID, PaperID, Title FROM paper')
    papers = cur.fetchall()
    print(papers)
    for paper in papers:
        print(paper)
    return render_template('authors.html', papers = papers)

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

        if usertype == 'Author':
            cur.execute('INSERT INTO author (AuthorID, FirstName, MiddleInitial, LastName, Affiliation, Department, Address, City, State, ZipCode, PhoneNumber, EmailAddress, Password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (authorid, fname, mname, lname, affil, department, address, city, state, zipCode, phone, email, password ))
            db.commit()

        else:
            cur.execute('INSERT INTO reviewer (ReviewerID, FirstName, MiddleInitial, LastName, Affiliation, Department, Address, City, State, ZipCode, PhoneNumber, EmailAddress, Password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (authorid, fname, mname, lname, affil, department, address, city, state, zipCode, phone, email, password ))
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
        
    return render_template('registerforreview.html')

@app.route('/reports')
def reports():
    cur.execute('select ReviewID, review.Paperid, Title, AppropriatenessOfTopic, TimelinessOfTopic, SupportiveEvidence, TechnicalQuality, ScopeOfCoverage, CitationOfPreviousWork, Originality, OrganizationOfPaper, ClarityOfMainMessage, Mechanics, SuitabilityForPresentation, PotentialInterestInTopic, OverallRating, ComfortLevelTopic, ComfortLevelAcceptability from review natural join paper') 
    papers = cur.fetchall()
    print(papers)
    for paper in papers:
        print(paper)
    return render_template('scorereport.html', papers = papers)

@app.route('/reviewpaper', methods=['GET', 'POST'])
def reviewpaper():
    msg = ''
    if request.method == 'POST':
        cur.execute("SELECT ReviewerID FROM reviewer WHERE EmailAddress = %s", [session['id']])
        reviewer_id = cur.fetchone()
        print(cur._last_executed)
        print('in request method')

        paper = request.form['paper_id']
        print(paper)
        value1 = request.form['Appropriateness']
        print(value1)
        value2 = request.form['Timeliness']
        print(value2)
        value3 = request.form['Supportive']
        print(value3)
        value4 = request.form['TechnicalQuality']
        print(value4)
        value5 = request.form['Scope']
        print(value5)
        value6 = request.form['Citations']
        print(value6)
        value7 = request.form['Originality']
        print(value7)
        value8 = request.form['Organization']
        print(value8)
        value9 = request.form['Clarity']
        print(value9)
        value10 = request.form['Mechanics']
        print(value10)
        value11 = request.form['Suitability']
        print(value11)
        value12 = request.form['PotentialInterest']
        print(value12)
        value13 = request.form['ComfortLevel']
        print(value13)
        value14 = request.form['ComfortLevelAccept']
        print(value14)
        value15 = request.form['overallrating']
        print(value15)

        cur.execute('''UPDATE review SET 
            AppropriatenessOfTopic = %s,
            TimelinessOfTopic = %s,
            SupportiveEvidence = %s,
            TechnicalQuality = %s,
            ScopeOfCoverage = %s,
            CitationOfPreviousWork = %s,
            Originality = %s,
            OrganizationOfPaper = %s,
            ClarityOfMainMessage = %s,
            Mechanics = %s,
            SuitabilityForPresentation = %s,
            PotentialInterestInTopic = %s,
            OverallRating = %s,
            ComfortLevelTopic = %s,
            ComfortLevelAcceptability = %s,
        WHERE
            ReviewerID = %s and PaperID = %s''', (value1, value2, value3, value4, value5, value6, value7, value8, value9, value10, value11, value12, value13, value14, value15, reviewer_id, paper))
        
        db.commit()
        msg = "Review Successfully Uploaded"
        return render_template('reviewpaper.html', msg = msg)

    return render_template('reviewpaper.html')

@app.route('/viewpaper')
def viewpaper():
    cur.execute("SELECT ReviewerID FROM reviewer WHERE EmailAddress = %s", [session['id']])
    reviewer_id = cur.fetchone()
    print(reviewer_id)
    print(cur._last_executed)
    print(reviewer_id)
    cur.execute('select paper.PaperID, Title, FilenameOriginal from paper natural join review where ReviewerID = %s', [reviewer_id[0]])
    print(cur._last_executed)
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
        cur.execute("SELECT ReviewerID FROM reviewer WHERE EmailAddress = %s", [session['id']])
        reviewer_id = cur.fetchone()
        print(reviewer_id)
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
            inputs = (new_val, reviewer_id[0])
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

        elif email == "admin@cpms" and zipcode == "12345":
            msg = 'Your Password is admin242'
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
            return render_template("distributepapers.html", msg = msg, reviewers = reviewers)


    return render_template("distributepapers.html")

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   # Redirect to login page
   return redirect(url_for('home'))

@app.route('/manageusers', methods=['GET', 'POST'])
def manageusers():
    msg = ''
    cur.execute('SELECT AuthorID, FirstName, LastName, EmailAddress from author UNION SELECT ReviewerID, FirstName, LastName, EmailAddress from reviewer')
    database = cur.fetchall()

    if request.method == "POST":
        print('submitted properly')
        userid = request.form['userid']
        print(userid)
        email = request.form['email']
        print(email)
        action = request.form['action']
        print(action)
        to_update = request.form['to_update']
        print(to_update)
        newvalue = request.form['updatedval']
        print(newvalue)
        password = request.form['password']
        print(password)
        stopsubs = request.form['stopsubmissions']
        print(stopsubs)

        cur.execute('SELECT * FROM author WHERE emailAddress = %s', [email])
        exists = cur.fetchone()
        if stopsubs == "yes":
            pass

        if exists:
            if action == "delete":
                cur.execute('DELETE FROM author WHERE EmailAddress = %s', [email])
                msg = 'Changes Successfully Made'
                return render_template('manageusers.html', database = database, msg = msg)
            else:
                statement1 = 'UPDATE author SET %s'
                fixed = statement1 % to_update
                statement2 = '= %s WHERE EmailAddress = %s'
                input = fixed + statement2
                print(input)
                inputvals = (newvalue, email)
                cur.execute(input, inputvals)
                print(cur._last_executed)
                print('Success')
                msg = 'Changes Successfully Made'
                return render_template('manageusers.html', database = database, msg = msg)

        else:
            if action == "delete":
                cur.execute('DELETE FROM reviewer WHERE EmailAddress = %s', [email])
                return render_template('manageusers.html', database = database)
            else:
                statement1 = 'UPDATE reviewer SET %s'
                fixed = statement1 % to_update
                statement2 = '= %s WHERE EmailAddress = %s'
                input = fixed + statement2
                print(input)
                inputvals = (newvalue, email)
                cur.execute(input, inputvals)
                print(cur._last_executed)
                print('Success')
                msg = 'Changes Successfully Made'
                return render_template('manageusers.html', database = database, msg = msg)

    return render_template('manageusers.html', database = database)

@app.route('/assignpapers', methods=['GET', 'POST'])
def assignpapers():
    msg = ''
    if request.method == "POST":
        paperid = request.form['paperid']
        print(paperid)
        reviewerid = request.form['reviewerID']
        print(reviewerid)

        reviewID = cur.execute("SELECT COUNT(*) FROM review")
        reviewID = cur.fetchone()[0]
        reviewID += 1

        cur.execute('INSERT INTO review(ReviewID, PaperID, ReviewerID) VALUES (%s, %s, %s)', (reviewID, paperid, reviewerid))
        print(cur._last_executed)
        msg = 'Paper Assigned to Reviewer'
        return render_template('assignpapers.html', msg = msg)

    return render_template('assignpapers.html')
