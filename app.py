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
    return "<h1>HOME</h1>"

@app.route('/customers', methods=["POST", "GET"])
def customers():
    if request.method == "GET":
      query = "SELECT * FROM Customers;"
      cur = mysql.connection.cursor()
      cur.execute(query)
      results = cur.fetchall()
    
    if request.method == "POST":
      if request.form.get("Add_Customer"):
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

      query = "INSERT INTO bsg_people (name, email, password) VALUES (%s, %s,%s,%s)"
      cur = mysql.connection.cursor()
      cur.execute(query, (name, email, password))
      mysql.connection.commit()

      return render_template("people.j2", data=results)
    
# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=8001, debug=True)
