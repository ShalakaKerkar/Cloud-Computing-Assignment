from flask import Flask, render_template, url_for
from flask import request, redirect
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('database.db')
conn.execute('drop table user')
conn.execute('CREATE TABLE IF NOT EXISTS user (username TEXT, password TEXT, email EMAIL, first_name TEXT, last_name TEXT, link TEXT)');

       

@app.route('/login', methods = ['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM user WHERE username = ? AND password = ?",(username,password))
        result = cur.fetchone()
    if(result):
        return render_template("home.html", result = result)
    return render_template("login.html", error_flag = True)

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            fname = request.form['fname']
            lname = request.form['lname']
            
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO user (username,password,email,first_name,last_name, link) VALUES (?,?,?,?,?,?)",(username,password,email,fname,lname, ''))
                con.commit()
            
            return render_template("home.html", result = [username, password, email, fname, lname, ])

        except BaseException as err:
            con.rollback()
            con.close()
       
    return render_template("register.html")
    
@app.route('/')
def init():
    return render_template('login.html')
    
if __name__ == '__main__':
    app.run()
