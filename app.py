from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
from dotenv import load_dotenv, find_dotenv
import os
import database.db_connector as db
import pdb

db_connection = db.connect_to_database()

# load_dotenv(find_dotenv())


app = Flask(__name__)

# app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
# app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
# app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD") 
# app.config['MYSQL_DB'] = os.environ.get("MYSQL_USER")
# app.config['MYSQL_USER'] = 'cs340_akinsm'
# app.config['MYSQL_PASSWORD'] = '1516'
# app.config['MYSQL_DB'] = 'cs340_akinsm'
# app.config['MYSQL_CURSORCLASS'] = "DictCursor"


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
        cur = db.execute_query(db_connection=db_connection, query=query)
        customer_data = cur.fetchall()
        return render_template("customers2.j2", data=customer_data)

    if request.method == "POST":
        if request.form.get("Add_Customer"):
            name = request.form["name"]
            email = request.form["email"]
            password = request.form["password"]
            query = "INSERT INTO Customers (name, email, password) VALUES (%s, %s, %s)"
            db.execute_query(db_connection=db_connection, query=query, query_params=(name, email, password))
        return redirect("/customers")

     
@app.route("/delete_customer/<int:id>")
def delete_customer(id):
  query1 = "SET foreign_key_checks=0;"
  query2 = "DELETE FROM Customers WHERE customer_id = '%s';"
  query3 = "SET foreign_key_checks=1;"
  db.execute_query(db_connection=db_connection, query=query1)
  db.execute_query(db_connection=db_connection, query=query2, query_params=(id,))

  # redirect back to customers page
  return redirect("/customers")

@app.route("/edit_customer/<int:id>", methods=["POST", "GET"])
def edit_customer(id):
   if request.method == "GET":
      # mySQL query to grab the info of the person with our passed id
      query = "SELECT * FROM Customers WHERE customer_id = %s;" #% (id)
      cur = db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
      customer_data = cur.fetchall()

      # render edit_people page passing our query data and homeworld data to the edit_people template
      return render_template("edit_customer.j2", data=customer_data)
   
   if request.method == "POST":
      # fire off if user clicks the 'Edit Person' button
      if request.form.get("Edit_Customer"):
         # grab user form inputs
        id = request.form["customer_id"]
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        query = "UPDATE Customers SET Customers.name = %s, Customers.email = %s, Customers.password = %s WHERE customer_id = %s"
        db.execute_query(db_connection=db_connection, query=query, query_params=(name, email, password, id))
        # redirect back to people page after we execute the update query
        return redirect("/customers")


@app.route('/orders', methods=["POST", "GET"])
def orders():
    if request.method == "GET":
        query = "SELECT * FROM Orders;"
        cur = db.execute_query(db_connection=db_connection, query=query)
        order_data = cur.fetchall()
        query2 = "SELECT * FROM Customers"
        cur2 = db.execute_query(db_connection=db_connection, query=query2)
        customers = cur2.fetchall()
        return render_template("orders.j2", data=order_data, customers=customers)

    if request.method == "POST":
        if request.form.get("Add_Order"):
            customer_id = request.form["customer_id"]
            order_date = request.form["order_date"]
            query = "INSERT INTO Orders (customer_id, order_date) VALUES (%s, %s)"
            db.execute_query(db_connection=db_connection, query=query, query_params=(customer_id, order_date))
        return redirect("/orders")


@app.route("/delete_order/<int:id>")
def delete_order(id):
  query1 = "SET foreign_key_checks=0;"
  query2 = "DELETE FROM Orders WHERE order_id = '%s';"
  query3 = "SET foreign_key_checks=1;"
  db.execute_query(db_connection=db_connection, query=query1)
  db.execute_query(db_connection=db_connection, query=query2, query_params=(id,))
  db.execute_query(db_connection=db_connection, query=query3)

  # redirect back to customers page
  return redirect("/orders")


@app.route("/edit_order/<int:id>", methods=["POST", "GET"])
def edit_order(id):
   if request.method == "GET":
      # mySQL query to grab the info of the person with our passed id
      query = "SELECT * FROM Orders WHERE order_id = %s;" #% (id)
      cur = db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
      order_data = cur.fetchall()

      # render edit_people page passing our query data and homeworld data to the edit_people template
      return render_template("edit_order.j2", data=order_data)
   
   if request.method == "POST":
      # fire off if user clicks the 'Edit Person' button
      if request.form.get("Edit_Order"):
         # grab user form inputs
        id = request.form["order_id"]
        customer_id = request.form["customer_id"]
        order_date = request.form["order_date"]
        query = "UPDATE Orders SET Orders.customer_id = %s, Orders.order_date = %s WHERE order_id = %s"
        db.execute_query(db_connection=db_connection, query=query, query_params=(customer_id, order_date, id))
        # redirect back to people page after we execute the update query
        return redirect("/orders")


@app.route('/products', methods=["POST", "GET"])
def products():
    if request.method == "GET":
        query = "SELECT * FROM Products;"
        cur = db.execute_query(db_connection=db_connection, query=query)
        product_data = cur.fetchall()
        query2 = "SELECT * FROM Scents;"
        cur2 = db.execute_query(db_connection=db_connection, query=query2)
        scent_data = cur2.fetchall()
        query3 = "SELECT * FROM Product_Types;"
        cur3 = db.execute_query(db_connection=db_connection, query=query3)
        product_type_data = cur3.fetchall()
        return render_template("products.j2", data=product_data, scents=scent_data, product_types=product_type_data)

    if request.method == "POST":
        if request.form.get("Add_Product"):
            scent = request.form["scent"]
            price = request.form["price"]
            product_type = request.form["product_type"]
            inventory = request.form["inventory"]
            query = "INSERT INTO Products (scent, price, product_type, inventory) VALUES (%s, %s, %s, %s)"
            db.execute_query(db_connection=db_connection, query=query, query_params=(scent, price, product_type, inventory))
        return redirect("/products")

@app.route("/delete_product/<int:id>")
def delete_product(id):
  query1 = "SET foreign_key_checks=0;"
  query2 = "DELETE FROM Products WHERE product_id = '%s';"
  query3 = "SET foreign_key_checks=1;"
  db.execute_query(db_connection=db_connection, query=query1)
  db.execute_query(db_connection=db_connection, query=query2, query_params=(id,))
  db.execute_query(db_connection=db_connection, query=query3)
  return redirect("/products")

      
@app.route("/edit_product/<int:id>", methods=["POST", "GET"])
def edit_product(id):
   if request.method == "GET":
      # mySQL query to grab the info of the person with our passed id
      query = "SELECT * FROM Products WHERE product_id = %s;" #% (id)
      cur = db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
      product_data = cur.fetchall()

      # render edit_people page passing our query data and homeworld data to the edit_people template
      return render_template("edit_product.j2", data=product_data)
   
   if request.method == "POST":
      # fire off if user clicks the 'Edit Person' button
      if request.form.get("Edit_Product"):
         # grab user form inputs
        id = request.form["product_id"]
        scent = request.form["scent"]
        price = request.form["price"]
        product_type = request.form["product_type"]
        inventory = request.form["inventory"]
        query = "UPDATE Products SET Products.scent = %s, Products.price = %s, Products.product_type = %s, Products.inventory = %s WHERE product_id = %s"
        db.execute_query(db_connection=db_connection, query=query, query_params=(scent, price, product_type, inventory, id))
        # redirect back to people page after we execute the update query
        return redirect("/products")


@app.route('/scents', methods=["POST", "GET"])
def scents():
    if request.method == "GET":
        query = "SELECT * FROM Scents;"
        cur = db.execute_query(db_connection=db_connection, query=query)
        scent_data = cur.fetchall()
        return render_template("scents.j2", data=scent_data)

    if request.method == "POST":
        if request.form.get("Add_Scent"):
            description = request.form["description"]
            query = "INSERT INTO Scents (description) VALUES (%s)"
            db.execute_query(db_connection=db_connection, query=query, query_params=(description,))
        return redirect("/scents")

@app.route("/delete_scent/<int:id>")
def delete_scent(id):
  query1 = "SET foreign_key_checks=0;"
  query2 = "DELETE FROM Scents WHERE scent_id = '%s';"
  query3 = "SET foreign_key_checks=1;"
  db.execute_query(db_connection=db_connection, query=query1)
  db.execute_query(db_connection=db_connection, query=query2, query_params=(id,))
  db.execute_query(db_connection=db_connection, query=query3)
  return redirect("/scents")

      
@app.route("/edit_scent/<int:id>", methods=["POST", "GET"])
def edit_scent(id):
   if request.method == "GET":
      # mySQL query to grab the info of the person with our passed id
      query = "SELECT * FROM Scents WHERE scent_id = %s;" #% (id)
      cur = db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
      scent_data = cur.fetchall()

      # render edit_people page passing our query data and homeworld data to the edit_people template
      return render_template("edit_scent.j2", data=scent_data)
   
   if request.method == "POST":
      # fire off if user clicks the 'Edit Person' button
      if request.form.get("Edit_Scent"):
         # grab user form inputs
        id = request.form["scent_id"]
        description = request.form["description"]
        query = "UPDATE Scents SET Scents.description = %s WHERE scent_id = %s"
        db.execute_query(db_connection=db_connection, query=query, query_params=(description, id))
        # redirect back to people page after we execute the update query
        return redirect("/scents")


@app.route('/product_types', methods=["POST", "GET"])
def product_types():
    if request.method == "GET":
        query = "SELECT * FROM Product_Types;"
        cur = db.execute_query(db_connection=db_connection, query=query)
        product_type_data = cur.fetchall()
        return render_template("product_types.j2", data=product_type_data)

    if request.method == "POST":
        if request.form.get("Add_Product_Type"):
            description = request.form["description"]
            query = "INSERT INTO Product_Types (description) VALUES (%s)"
            db.execute_query(db_connection=db_connection, query=query, query_params=(description,))
        return redirect("/product_types")

@app.route("/delete_product_type/<int:id>")
def delete_product_type(id):
  query1 = "SET foreign_key_checks=0;"
  query2 = "DELETE FROM Product_Types WHERE product_type_id = '%s';"
  query3 = "SET foreign_key_checks=1;"
  db.execute_query(db_connection=db_connection, query=query1)
  db.execute_query(db_connection=db_connection, query=query2, query_params=(id,))
  db.execute_query(db_connection=db_connection, query=query3)
  return redirect("/product_types")

      
@app.route("/edit_product_type/<int:id>", methods=["POST", "GET"])
def edit_product_type(id):
   if request.method == "GET":
      # mySQL query to grab the info of the person with our passed id
      query = "SELECT * FROM Product_Types WHERE product_type_id = %s;" #% (id)
      cur = db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
      product_type_data = cur.fetchall()

      # render edit_people page passing our query data and homeworld data to the edit_people template
      return render_template("edit_product_type.j2", data=product_type_data)
   
   if request.method == "POST":
      # fire off if user clicks the 'Edit Person' button
      if request.form.get("Edit_Product_Type"):
         # grab user form inputs
        id = request.form["product_type_id"]
        description = request.form["description"]
        query = "UPDATE Product_Types SET Product_Types.description = %s WHERE product_type_id = %s"
        db.execute_query(db_connection=db_connection, query=query, query_params=(description, id))
        # redirect back to people page after we execute the update query
        return redirect("/product_types")
    

# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    # app.run(port=8000, debug=True)
    app.run(port=8006, debug=True)
