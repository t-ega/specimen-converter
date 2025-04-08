import tkinter as tk
from tkinter import messagebox
import sqlite3

def init_db():
    conn = sqlite3.connect("specimen_data.db")
    cursor = conn.cursor()
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

def convert_size(measured_size, magnification, target_unit):
    actual_size_mm = measured_size / magnification

    conversion_factors = {
        "mm": 1,
        "µm": 1000,
        "um": 1000,
        "nm": 1_000_000,
        "cm": 0.1,
        "m": 0.001
    }

    if target_unit not in conversion_factors:
        return None

    return actual_size_mm * conversion_factors[target_unit]

def save_to_db(username, measured_size, magnification):
    conn = sqlite3.connect("specimen_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO specimen_records (username, measured_size, magnification)
        VALUES (?, ?, ?)
    """, (username, measured_size, magnification))
    conn.commit()
    conn.close()

def calculate():
    username = entry_username.get().strip()
    try:
        measured = float(entry_measured.get())
        magnification = float(entry_magnification.get())
        target_unit = unit_var.get()

        if not username:
            messagebox.showwarning("Missing username", "Please enter your name.")
            return

        result = convert_size(measured, magnification, target_unit)
        if result is None:
            messagebox.showerror("Unsupported unit", f"Unit '{target_unit}' is not supported.")
            return

        label_result.config(text=f"Actual size: {result:.4f} {target_unit}")

        save_to_db(username, measured, magnification)
        messagebox.showinfo("Success", "Data saved successfully!")

    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numeric values.")

# GUI Setup
root = tk.Tk()
root.title("Specimen Size Converter")
root.geometry("350x350")
root.resizable(False, False)

tk.Label(root, text="Username:").pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Measured size (mm):").pack(pady=5)
entry_measured = tk.Entry(root)
entry_measured.pack()

tk.Label(root, text="Magnification:").pack(pady=5)
entry_magnification = tk.Entry(root)
entry_magnification.pack()

tk.Label(root, text="Convert to unit:").pack(pady=5)
unit_var = tk.StringVar(root)
unit_var.set("nm")  # default unit

unit_options = ["mm", "µm", "nm", "cm", "m"]
unit_menu = tk.OptionMenu(root, unit_var, *unit_options)
unit_menu.pack()

tk.Button(root, text="Convert & Save", command=calculate).pack(pady=10)

label_result = tk.Label(root, text="Actual size: --")
label_result.pack(pady=5)

init_db()
root.mainloop()
