from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD") 
app.config['MYSQL_DB'] = os.environ.get("MYSQL_USER")
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)


# Routes
@app.route('/')
def root():
    query = "SELECT * FROM Customers;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    results = cur.fetchall()

    return "<h1>MySQL Results</h1>" + str(results[0])


# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=8001, debug=True)
