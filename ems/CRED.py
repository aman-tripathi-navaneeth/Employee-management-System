import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
conn = sqlite3.connect("employees.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT NOT NULL
    )
""")
conn.commit()

# Functions
def create_employee():
    eid = entry_id.get()
    name = entry_name.get()
    role = entry_role.get()

    try:
        cursor.execute("INSERT INTO employees (id, name, role) VALUES (?, ?, ?)", (eid, name, role))
        conn.commit()
        messagebox.showinfo("Success", "Employee added successfully!")
        clear_fields()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Employee ID already exists!")

def read_employee():
    eid = entry_id.get()
    cursor.execute("SELECT * FROM employees WHERE id = ?", (eid,))
    emp = cursor.fetchone()
    if emp:
        entry_name.delete(0, tk.END)
        entry_name.insert(0, emp[1])
        entry_role.delete(0, tk.END)
        entry_role.insert(0, emp[2])
    else:
        messagebox.showerror("Error", "Employee not found!")

def update_employee():
    eid = entry_id.get()
    name = entry_name.get()
    role = entry_role.get()

    cursor.execute("UPDATE employees SET name = ?, role = ? WHERE id = ?", (name, role, eid))
    if cursor.rowcount == 0:
        messagebox.showerror("Error", "Employee not found!")
    else:
        conn.commit()
        messagebox.showinfo("Success", "Employee updated successfully!")
        clear_fields()

def delete_employee():
    eid = entry_id.get()
    cursor.execute("DELETE FROM employees WHERE id = ?", (eid,))
    if cursor.rowcount == 0:
        messagebox.showerror("Error", "Employee not found!")
    else:
        conn.commit()
        messagebox.showinfo("Success", "Employee deleted successfully!")
        clear_fields()

def clear_fields():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_role.delete(0, tk.END)

# GUI setup
root = tk.Tk()
root.title("Employee Management System")

tk.Label(root, text="Employee ID").grid(row=0, column=0, padx=10, pady=5)
tk.Label(root, text="Name").grid(row=1, column=0, padx=10, pady=5)
tk.Label(root, text="Role").grid(row=2, column=0, padx=10, pady=5)

entry_id = tk.Entry(root)
entry_name = tk.Entry(root)
entry_role = tk.Entry(root)

entry_id.grid(row=0, column=1, padx=10, pady=5)
entry_name.grid(row=1, column=1, padx=10, pady=5)
entry_role.grid(row=2, column=1, padx=10, pady=5)

tk.Button(root, text="Create", command=create_employee).grid(row=3, column=0, pady=10)
tk.Button(root, text="Read", command=read_employee).grid(row=3, column=1)
tk.Button(root, text="Update", command=update_employee).grid(row=4, column=0)
tk.Button(root, text="Delete", command=delete_employee).grid(row=4, column=1)
tk.Button(root, text="Clear", command=clear_fields).grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()

# Close the DB connection when the app exits
conn.close()
