from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
from 
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
    print(os.environ.get("MYSQL_PASSWORD"))
    return render_template("home.j2")

@app.route('/customers', methods=["POST", "GET"])
def customers():
    if request.method == "GET":
      query = "SELECT * FROM Customers;"
      cur = mysql.connection.cursor()
      cur.execute(query)
      results = cur.fetchall()
      print(results)
      return render_template("customers.j2", data=results)
    
    if request.method == "POST":
      if request.form.get("Add_Customer"):
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        query = "INSERT INTO Customers (name, email, password) VALUES (%s, %s,%s);"
        cur = mysql.connection.cursor()
        cur.execute(query, (name, email, password))
        mysql.connection.commit()
        return redirect("/customers")

        

     
@app.route("/delete_customer/<int:id>")
def delete_customer(id):
  query1 = "SET foreign_key_checks=0;"
  query2 = "DELETE FROM Customers WHERE customer_id = '%s';"
  query3 = "SET foreign_key_checks=1;"
  cur = mysql.connection.cursor()
  cur.execute(query1)
  cur.execute(query2, (id,))
  cur.execute(query3)
  mysql.connection.commit()

  # redirect back to customers page
  return redirect("/customers")

@app.route("/edit_customer/<int:id>", methods=["POST", "GET"])
def edit_customer(id):
   if request.method == "GET":
      # mySQL query to grab the info of the person with our passed id
      query = "SELECT * FROM Customers WHERE customer_id = %s;" % (id)
      cur = mysql.connection.cursor()
      cur.execute(query)
      data = cur.fetchall()

      # render edit_people page passing our query data and homeworld data to the edit_people template
      return render_template("edit_customer.j2", data=data)
   
   if request.method == "POST":
      # fire off if user clicks the 'Edit Person' button
      if request.form.get("Edit_Customer"):
         # grab user form inputs
        print("keys", request.form)
        id = request.form["customer_id"]
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        print("stats", id, name, email, password)
        
        query = "UPDATE Customers SET Customers.name = %s, Customers.email = %s, Customers.password = %s WHERE customer_id = %s"
        cur = mysql.connection.cursor()
        attributes = (name, email, password, id)
        cur.execute(query, attributes)
        mysql.connection.commit()

            # redirect back to people page after we execute the update query
        return redirect("/customers")

      
    
# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    # app.run(port=8000, debug=True)
    app.run(port=8003, debug=True)
