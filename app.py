from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect("students.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER
        )
    """)
    conn.close()

init_db()

# Home Page
@app.route("/")
def index():
    conn = sqlite3.connect("students.db")
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template("index.html", students=students)

# Add Student
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]

        conn = sqlite3.connect("students.db")
        conn.execute("INSERT INTO students (name, age) VALUES (?, ?)", (name, age))
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add.html")

# Delete Student
@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("students.db")
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
