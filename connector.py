import MySQLdb as mdb

DBNAME="cpms"  # database name
#DBPORT=3306      # database port
DBHOST="localhost"  # database host
DBUSER="root"  # database user
DBPASS="root"  # database password

db= mdb.connect(DBHOST, DBUSER, DBPASS, DBNAME)
cur = db.cursor()

username = 'pbenedtti0@wix.com'
password = 'grl3L6Z0KBT2'
# Check if account exists using MySQL
cur.execute('SELECT emailAddress, password FROM reviewer WHERE emailAddress= %s AND Password = %s UNION SELECT emailAddress, password FROM author WHERE emailAddress= %s AND Password = %s', (username, password, username, password))
# Fetch one record and return result
account = cur.fetchone()
print(account)

'SELECT emailAddress, password FROM reviewer WHERE emailAddress= %s AND Password = %s UNION SELECT emailAddress, password FROM author WHERE emailAddress= %s AND Password = %s'

'SELECT * FROM author WHERE AuthorID = %s AND Password = %s'