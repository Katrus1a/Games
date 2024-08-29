import tkinter as tk
from tkinter import messagebox
import sqlite3
from ursina import *

app=Ursina()

background = Entity(model='quad', color=color.magenta, scale=100, z=10, y=15)

camera.orthographic=True
camera.fov=18

player=Entity(model='quad', collider='box', texture='assets/squre.png', scale=(5, 5, 5))

ground=Entity(model='cube', color=color.yellow, y=-1, origin_y=.5, scale=(200, 25, 1), collider='box', texture='white_cube')
diam=[]
plates=[]

def new(val):
    new1=Entity(model='diamond', color=color.red, y=1, texture='white_cube', x=val, collider='mesh', scale=(2, 2, 2))
    new2=duplicate(new1, y=2.35, x=val + 1, scale=0.8)

    diam.extend((new1, new2))
    if val % 60==0:
        for i in range(5):
            e=Entity(model='cube',
                       y=i-0.2, x=val+5+i*15,
                       scale_x=10,
                       scale_y=2,
                       collider='box',
                       color=color.yellow,
                       texture='white_cube')
            plates.append(e)
    invoke(new, val=val+10, delay=1)

new(30)

def update():
    for ob in diam:
        ob.x-=20*time.dt
    for ob in plates:
        ob.x-=20*time.dt

    if not player.intersects().hit:
        player.y-=20*time.dt
        player.y=max(-5, player.y)
        t=player.intersects()
        if t.hit:
            for en in t.entities:
                if en.color==color.violet:
                    print("You Lose!")

def input(key):
    if key=="space":
        if player.intersects().hit:
            player.animate_y(player.y+10, duration=0.3, curve=curve.out_sine)
            player.animate_rotation_z(player.rotation_z+180, duration=0.5, curve=curve.linear)
            dust=Entity(model=Circle(), scale=-3, color=color.smoke, position=player.position)
            dust.animate_scale(2, duration=3, curve=curve.linear)
            dust.fade_out(duration=1)

app.run()


# conn=sqlite3.connect('users.db')
# cursor=conn.cursor()
#
# cursor.execute('''CREATE TABLE IF NOT EXISTS users
#                   (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
# conn.commit()
#
# def register_user():
#     username=username_entry.get()
#     password=password_entry.get()
#     confirm_password=confirm_password_entry.get()
#
#     if not username or not password or not confirm_password:
#         messagebox.showwarning("Error", "All fields must be filled!")
#     elif password!=confirm_password:
#         messagebox.showwarning("Error", "Passwords do not match!")
#     else:
#         try:
#             cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
#             conn.commit()
#             messagebox.showinfo("Success", f"User {username} registered successfully!")
#             display_users()
#             main_window.destroy()
#         except sqlite3.IntegrityError:
#             messagebox.showwarning("Error", f"User {username} already exists!")
#
# def display_users():
#     users_window=tk.Toplevel(main_window)
#     users_window.title("Registered Users")
#     users_window.geometry("300x400")
#     users_window.configure(bg="#000000")
#
#     cursor.execute("SELECT username FROM users")
#     users=cursor.fetchall()
#
#     for user in users:
#         user_label=tk.Label(users_window, text=user[0], font=label_font, fg="#ffcc00", bg="#000000")
#         user_label.pack(pady=5)
#
# main_window=tk.Tk()
# main_window.title("Geometry Dash Registration")
# main_window.geometry("500x500")
# main_window.configure(bg="#000000")
#
# label_font=("Arial", 16, "bold")
# title_font=("Arial", 26, "bold")
# entry_bg="#333333"
# entry_fg="#ffffff"
# button_bg="#ffcc00"
# button_fg="#ffffff"
# outline_fg="#000000"
#
# def create_label(text, color, bg_color, root, font, center=False):
#     label=tk.Label(root, text=text, font=font, fg=color, bg=bg_color)
#     if center:
#         label.pack(anchor='center', pady=20)
#     else:
#         label.pack(anchor='w', padx=50, pady=5)
#     return label
#
# create_label("Registration", "#ffcc00", "#000000", main_window, title_font, center=True)
#
# create_label("Username:", "#00ff66", "#000000", main_window, label_font)
# username_entry=tk.Entry(main_window, font=label_font, bg=entry_bg, fg=entry_fg)
# username_entry.pack(pady=10, padx=50, fill='x')
#
# create_label("Password:", "#31f2f5", "#000000", main_window, label_font)
# password_entry=tk.Entry(main_window, show="*", font=label_font, bg=entry_bg, fg=entry_fg)
# password_entry.pack(pady=10, padx=50, fill='x')
#
# create_label("Confirm Password:", "#6851fc", "#000000", main_window, label_font)
# confirm_password_entry=tk.Entry(main_window, show="*", font=label_font, bg=entry_bg, fg=entry_fg)
# confirm_password_entry.pack(pady=10, padx=50, fill='x')
#
# register_button=tk.Button(main_window, text="Register", font=(label_font[0], label_font[1], 'bold'),
#                             bg=button_bg, fg=button_fg, command=register_user, width=20,
#                             highlightbackground=outline_fg, highlightthickness=2)
# register_button.pack(pady=50)
#
# main_window.mainloop()
#
# conn.close()
