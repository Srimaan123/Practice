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
conn.close()
app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def hello():
    conn = init()
    cursor = conn.cursor()
    if request.method == "POST":
        operation = request.form.get("operation")
        if operation == "change-status":
            id = request.form.get("id")
            print(id)
            cursor.execute("SELECT * FROM tasks WHERE id=?",(id,))
            task = cursor.fetchone()
            print(task)
            current_status = task[2]
            new_status = 0 if current_status == 1 else 1
            print("new status",new_status)
            cursor.execute("UPDATE tasks SET status=? WHERE id=?",(new_status,id))
            conn.commit()
            conn.close()
            return redirect("/")
        else:
            task = request.form.get("task")
            status = 0
            cursor.execute("INSERT INTO tasks(task,status) VALUES(?,?)",(task,status))
            conn.commit()
            conn.close()
            return redirect("/")
    else:
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        conn.close()
        return render_template("index.html",tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)
    