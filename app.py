from flask import Flask, render_template, request, redirect, flash
import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.secret_key = "secret"

conversion_factors = {
    "mm": 1,
    "µm": 1000,
    "um": 1000,
    "nm": 1_000_000,
    "cm": 0.1,
    "m": 0.001
}

def init_db():
    conn = sqlite3.connect("specimen_data.db")
    cursor = conn.cursor()
    print('Creating table')
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS specimen_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            measured_size REAL NOT NULL,
            magnification REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def convert_size(measured, magnification, unit):
    return (measured / magnification) * conversion_factors[unit]

def get_all_records():
    conn = sqlite3.connect("specimen_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, measured_size, magnification FROM specimen_records")
    records = cursor.fetchall()
    conn.close()
    return records

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    username = ""
    target_unit = "nm"

    if request.method == "POST":
        try:
            username = request.form["username"]
            measured = float(request.form["measured_size"])
            magnification = float(request.form["magnification"])
            target_unit = request.form["unit"]

            result = round(convert_size(measured, magnification, target_unit), 4)

            # Save to DB
            conn = sqlite3.connect("specimen_data.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO specimen_records (username, measured_size, magnification)
                VALUES (?, ?, ?)
            """, (username, measured, magnification))
            conn.commit()
            conn.close()

            flash("Conversion and save successful!")

        except Exception as e:
            flash("Error: " + str(e))

    records = get_all_records()

    return render_template(
        "index.html",
        result=result,
        username=username,
        selected_unit=target_unit,
        records=records,
        conversion_factors=conversion_factors
    )


init_db()
if __name__ == "__main__":
    port = os.environ.get('PORT') or 4000
    app.run(debug=True, port=port)
