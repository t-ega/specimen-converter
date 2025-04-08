import tkinter as tk
from tkinter import messagebox

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

def calculate():
    try:
        measured = float(entry_measured.get())
        magnification = float(entry_magnification.get())
        target_unit = unit_var.get()

        result = convert_size(measured, magnification, target_unit)

        if result is None:
            messagebox.showerror("Error", f"Unsupported unit: {target_unit}")
        else:
            label_result.config(text=f"Actual size: {result:.4f} {target_unit}")
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter numeric values for size and magnification.")

root = tk.Tk()
root.title("Specimen Size Converter")
root.geometry("320x250")
root.resizable(False, False)

tk.Label(root, text="Measured size (mm):").pack(pady=5)
entry_measured = tk.Entry(root)
entry_measured.pack()

tk.Label(root, text="Magnification:").pack(pady=5)
entry_magnification = tk.Entry(root)
entry_magnification.pack()

tk.Label(root, text="Convert to unit:").pack(pady=5)
unit_var = tk.StringVar(root)
unit_var.set("nm")  # Default unit

unit_options = ["mm", "µm", "nm", "cm", "m"]
unit_menu = tk.OptionMenu(root, unit_var, *unit_options)
unit_menu.pack()

tk.Button(root, text="Convert", command=calculate).pack(pady=10)

label_result = tk.Label(root, text="Actual size: --")
label_result.pack(pady=5)

root.mainloop()
