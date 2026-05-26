from flask import Flask,render_template,request,redirect
import sqlite3

def init():
    return sqlite3.connect("tasks.db")

conn = init()
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY,
    task TEXT,
    status BOOLEAN
);
''')
conn.commit()
app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def hello():
    conn = init()
    cursor = conn.cursor()
    if request.method == "POST":
        return "none"
    else:
        tasks = cursor.execute("SELECT * FROM tasks")
        return render_template("index.html",tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)
    