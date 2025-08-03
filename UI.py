import tkinter as tk
from tkinter import messagebox, filedialog
import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize Database
def init_db():
    conn = sqlite3.connect('mail_app.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY,
                    email TEXT,
                    password TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS sent_emails (
                    id INTEGER PRIMARY KEY,
                    recipient TEXT,
                    subject TEXT,
                    message TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    conn.close()

# Save Login
def save_settings():
    conn = sqlite3.connect('mail_app.db')
    c = conn.cursor()
    c.execute("DELETE FROM settings")
    c.execute("INSERT INTO settings (email, password) VALUES (?, ?)",
              (email_entry.get(), password_entry.get()))
    conn.commit()
    conn.close()
    messagebox.showinfo("Saved", "Settings saved successfully")

# Load Settings
def load_settings():
    conn = sqlite3.connect('mail_app.db')
    c = conn.cursor()
    c.execute("SELECT email, password FROM settings LIMIT 1")
    row = c.fetchone()
    conn.close()
    if row:
        email_entry.insert(0, row[0])
        password_entry.insert(0, row[1])

# Compose Email
def send_email():
    try:
        msg = MIMEMultipart()
        msg['From'] = email_entry.get()
        msg['To'] = to_entry.get()
        msg['Subject'] = subject_entry.get()
        body = message_text.get("1.0", tk.END)
        msg.attach(MIMEText(body, 'plain'))

        # Use default Gmail SMTP settings
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_entry.get(), password_entry.get())
        text = msg.as_string()
        server.sendmail(email_entry.get(), to_entry.get(), text)
        server.quit()

        # Save sent email
        conn = sqlite3.connect('mail_app.db')
        c = conn.cursor()
        c.execute("INSERT INTO sent_emails (recipient, subject, message) VALUES (?, ?, ?)",
                  (to_entry.get(), subject_entry.get(), body))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Email sent successfully")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# UI Setup
root = tk.Tk()
root.title("Mail Application")
root.geometry("500x600")

# SMTP Configuration Section
tk.Label(root, text="Email Account Setup", font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(root, text="Email").pack()
email_entry = tk.Entry(root, width=50)
email_entry.pack()

tk.Label(root, text="Password").pack()
password_entry = tk.Entry(root, show="*", width=50)
password_entry.pack()

tk.Button(root, text="Save Settings", command=save_settings).pack(pady=10)

# Email Sending Section
tk.Label(root, text="Send Email", font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(root, text="To").pack()
to_entry = tk.Entry(root, width=50)
to_entry.pack()

tk.Label(root, text="Subject").pack()
subject_entry = tk.Entry(root, width=50)
subject_entry.pack()

tk.Label(root, text="Message").pack()
message_text = tk.Text(root, height=10, width=60)
message_text.pack()

tk.Button(root, text="Send Message", command=send_email).pack(pady=10)

# Start App
init_db()
load_settings()
root.mainloop()