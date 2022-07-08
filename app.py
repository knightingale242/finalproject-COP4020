from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/scorebreakdown')
def reports():
    return render_template('scorebreakdown.html')

@app.route('/welcome')
def welcome():
    return render_template('homepage.html')

@app.route('/register')
def register():
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

if __name__ == "__main__":
    app.run(port='8082')
