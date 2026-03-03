import tkinter as tk
from tkinter import ttk
import re
import math
import random
import string


#  PASSWORD ANALYSIS #

def check_password():
    password = entry.get()
    score = 0
    feedback = []

    #  Length Check 
    if len(password) >= 12:
        score += 1
    else:
        feedback.append("Use at least 12 characters")

    #  Character Type Checks
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letter")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letter")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Add number")

    if any(char in string.punctuation for char in password):
        score += 1
    else:
        feedback.append("Add special character")

    #  Percentage 
    percentage = int((score / 5) * 100)
    progress["value"] = percentage

    #  Entropy Calculation (Safe Professional Method) 
    charset = 0
    if re.search(r"[a-z]", password): charset += 26
    if re.search(r"[A-Z]", password): charset += 26
    if re.search(r"[0-9]", password): charset += 10
    if any(char in string.punctuation for char in password):
        charset += len(string.punctuation)

    entropy = 0
    crack_time = "Very Fast"

    if charset > 0:
        entropy = round(len(password) * math.log2(charset), 2)

        attempts_per_second = 10**9
        seconds = (2 ** entropy) / attempts_per_second

        if seconds < 60:
            crack_time = f"{round(seconds,2)} seconds"
        elif seconds < 3600:
            crack_time = f"{round(seconds/60,2)} minutes"
        elif seconds < 86400:
            crack_time = f"{round(seconds/3600,2)} hours"
        elif seconds < 31536000:
            crack_time = f"{round(seconds/86400,2)} days"
        else:
            crack_time = f"{round(seconds/31536000,2)} years"

    # Strength Level 
    if score <= 2:
        strength = "Weak "
        color = "red"
    elif score <= 4:
        strength = "Medium "
        color = "orange"
    else:
        strength = "Strong "
        color = "lime"

    #  Final Output 
    result_text = f"""
Strength: {strength}
Score: {percentage}%
Entropy: {entropy} bits
Estimated Crack Time: {crack_time}

Suggestions:
"""
    if feedback:
        for item in feedback:
            result_text += f"- {item}\n"
    else:
        result_text += "- Excellent password structure\n"

    result_label.config(text=result_text, fg=color)


#  UTILITIES  #

def toggle_password():
    entry.config(show="" if entry.cget("show") == "*" else "*")


def clear_all():
    entry.delete(0, tk.END)
    result_label.config(text="")
    progress["value"] = 0


def generate_password():
    # Guaranteed complexity password
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]

    characters = string.ascii_letters + string.digits + string.punctuation
    password += [random.choice(characters) for _ in range(10)]

    random.shuffle(password)
    generated = ''.join(password)

    entry.delete(0, tk.END)
    entry.insert(0, generated)


#  GUI  #

window = tk.Tk()
window.title("Saniya Cyber Shield 🔐")
window.geometry("520x650")
window.configure(bg="black")

title = tk.Label(
    window,
    text="🔐 Advanced Password Intelligence Tool",
    fg="lime",
    bg="black",
    font=("Arial", 16, "bold")
)
title.pack(pady=15)

entry = tk.Entry(window, show="*", width=35, font=("Arial", 12))
entry.pack(pady=10)

tk.Button(window, text="Check Strength", command=check_password, bg="lime").pack(pady=5)
tk.Button(window, text="Show / Hide Password", command=toggle_password).pack(pady=5)
tk.Button(window, text="Generate Secure Password", command=generate_password).pack(pady=5)
tk.Button(window, text="Clear", command=clear_all).pack(pady=5)

progress = ttk.Progressbar(window, length=380, mode='determinate')
progress.pack(pady=15)

result_label = tk.Label(window, text="", bg="black", justify="left", font=("Arial", 11))
result_label.pack(pady=15)

window.mainloop()