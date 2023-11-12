import os
from flask import Flask, render_template, request
import mysql.connector
from dotenv import load_dotenv

load_dotenv(verbose=True)

app = Flask(__name__)

import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    database=os.getenv("DATABASE"),
    port='3306',
    charset='utf8'
)

cur = conn.cursor()

@app.route('/')
def show_word_table():
    req = request.args
    name = req.get("name")

    cur.execute("SELECT * FROM word where name=%s", (name,))
    data = cur.fetchall()

    return render_template('table.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)