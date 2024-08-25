import tkinter as tk
from tkinter import messagebox

def register_user():
    username=username_entry.get()
    password=password_entry.get()
    confirm_password=confirm_password_entry.get()

    if not username or not password or not confirm_password:
        messagebox.showwarning("Error", "All fields must be filled!")
    elif password != confirm_password:
        messagebox.showwarning("Error", "Passwords do not match!")
    else:
        messagebox.showinfo("Success", f"User {username} registered successfully!")
        main_window.destroy()
        
main_window=tk.Tk()
main_window.title("Geometry Dash Registration")
main_window.geometry("500x500")
main_window.configure(bg="#000000")

label_font=("Arial", 16, "bold")
title_font=("Arial", 26, "bold")
entry_bg="#333333"
entry_fg="#ffffff"
button_bg="#ffcc00"
button_fg="#ffffff"
outline_fg="#000000"

def create_label(text, color, bg_color, root, font, center=False):
    label=tk.Label(root, text=text, font=font, fg=color, bg=bg_color)
    if center:
        label.pack(anchor='center', pady=20)
    else:
        label.pack(anchor='w', padx=50, pady=5)
    return label

create_label("Registration", "#ffcc00", "#000000", main_window, title_font, center=True)

create_label("Username:", "#00ff66", "#000000", main_window, label_font)
username_entry=tk.Entry(main_window, font=label_font, bg=entry_bg, fg=entry_fg)
username_entry.pack(pady=10, padx=50, fill='x')

create_label("Password:", "#31f2f5", "#000000", main_window, label_font)
password_entry=tk.Entry(main_window, show="*", font=label_font, bg=entry_bg, fg=entry_fg)
password_entry.pack(pady=10, padx=50, fill='x')

create_label("Confirm Password:", "#6851fc", "#000000", main_window, label_font)
confirm_password_entry=tk.Entry(main_window, show="*", font=label_font, bg=entry_bg, fg=entry_fg)
confirm_password_entry.pack(pady=10, padx=50, fill='x')

register_button=tk.Button(main_window, text="Register", font=(label_font[0], label_font[1], 'bold'),
                            bg=button_bg, fg=button_fg, command=register_user, width=20,
                            highlightbackground=outline_fg, highlightthickness=2)
register_button.pack(pady=50)

main_window.mainloop()
