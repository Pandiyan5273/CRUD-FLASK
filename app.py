from flask import Flask, render_template, url_for, redirect, request, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'abc123'

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Anbu@1234",
        database="crud"
    )

@app.route('/')
def home():
    con = get_db_connection()
    cur = con.cursor(dictionary=True)
    sql = "SELECT * FROM student"
    cur.execute(sql)
    res = cur.fetchall()
    cur.close()
    con.close()
    return render_template("home.html", datas=res)

@app.route('/addusers', methods=['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        # Get both age and name from the form
        name = request.form['name']
        age = request.form['age']
        
        # Connect to the database
        con = get_db_connection()
        cur = con.cursor()

        # Insert both name and age into the database
        sql = "INSERT INTO student (name, AGE) VALUES (%s, %s)"
        cur.execute(sql, (name, age))
        con.commit()

        # Close the connection
        cur.close()
        con.close()

        # Flash success message and redirect to home
        flash('User added successfully')
        return redirect(url_for("home"))
    
    # Render the add user form (GET request)
    return render_template("addusers.html")

@app.route('/edituser/<string:id>', methods=['GET', 'POST'])
def edituser(id):
    con = get_db_connection()
    cur = con.cursor(dictionary=True)
    if request.method == 'POST':
        age = request.form['age']
        sql = "UPDATE student SET AGE=%s WHERE ID=%s"
        cur.execute(sql, (age, id))
        con.commit()
        cur.close()
        con.close()
        flash("User updated successfully")
        return redirect(url_for("home"))
    
    sql = "SELECT * FROM student WHERE ID=%s"
    cur.execute(sql, (id,))
    res = cur.fetchone()
    cur.close()
    con.close()
    return render_template("editusers.html", datas=res)

@app.route('/deleteuser/<string:id>', methods=['GET', 'POST'])
def deleteuser(id):
    con = get_db_connection()
    cur = con.cursor()
    sql = "DELETE FROM student WHERE ID=%s"
    cur.execute(sql, (id,))
    con.commit()
    cur.close()
    con.close()
    flash("User deleted successfully")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
