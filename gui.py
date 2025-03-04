import tkinter as tk
from tkinter import messagebox
from src.database import store_password, retrieve_password, list_services
from src.auth import verify_master_password
from src.password_generator import generate_password

def save_password():
    service = service_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    master = master_entry.get()

    if not verify_master_password(master):
        return

    if service and username and password:
        store_password(master, service, username, password)
        messagebox.showinfo("Success", "Password saved!")
        service_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please fill in all fields!")

def get_password():
    service = service_entry.get()
    master = master_entry.get()

    if not verify_master_password(master):
        return

    if service:
        result = retrieve_password(master, service)
        messagebox.showinfo("Retrieved Password", result)
    else:
        messagebox.showerror("Error", "Please enter a service name!")

def generate_strong_password():
    password_entry.delete(0, tk.END)
    password_entry.insert(0, generate_password(16))

# GUI Setup
root = tk.Tk()
root.title("Password Manager")

tk.Label(root, text="Service:").grid(row=0, column=0)
tk.Label(root, text="Username:").grid(row=1, column=0)
tk.Label(root, text="Password:").grid(row=2, column=0)
tk.Label(root, text="Master Password:").grid(row=3, column=0)

service_entry = tk.Entry(root)
username_entry = tk.Entry(root)
password_entry = tk.Entry(root)
master_entry = tk.Entry(root, show="*")

service_entry.grid(row=0, column=1)
username_entry.grid(row=1, column=1)
password_entry.grid(row=2, column=1)
master_entry.grid(row=3, column=1)

tk.Button(root, text="Save Password", command=save_password).grid(row=4, column=0)
tk.Button(root, text="Retrieve Password", command=get_password).grid(row=4, column=1)
tk.Button(root, text="Generate Password", command=generate_strong_password).grid(row=5, column=1)

root.mainloop()
