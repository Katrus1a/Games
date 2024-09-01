import tkinter as tk
from tkinter import messagebox
import sqlite3
from ursina import *

def start_game():
    app=Ursina()

    background=Entity(model='quad', color=color.magenta, scale=100, z=10, y=15)
    camera.orthographic=True
    camera.fov=18

    player=Entity(model='quad', collider='box', texture='assets/squre.png', scale=(2, 2, 2))
    ground=Entity(model='cube', color=color.yellow, y=-1, origin_y=.5, scale=(100, 10, 1), collider='box', texture='white_cube')
    bottom_background=Entity(model='quad', color=color.magenta, scale=(100, 20), y=-10, z=9)

    diam=[]
    plates=[]
    obstacles=[]
    score=0
    is_game_over=False
    game_over_text=None
    score_text=Text(text=f'Score: {score}', position=(0.7, 0.45), scale=2, color=color.white)

    def new(val):
        new1=Entity(model='diamond', color=color.red, y=2, texture='white_cube', x=val, collider='mesh', scale=(1, 1, 1))
        new2=duplicate(new1, y=3.35, x=val+1, scale=0.6)
        diam.extend((new1, new2))

        if val%60==0:
            for i in range(5):
                e=Entity(model='cube', y=i-0.2, x=val+5+i*15, scale_x=5, scale_y=1, collider='box', color=color.yellow, texture='white_cube')
                plates.append(e)

        if val%20==0:
            obs=Entity(model='quad', color=color.red, scale=(1, 3), x=val, y=-1, collider='box', texture='white_cube')
            obstacles.append(obs)

        invoke(new, val=val+10, delay=1)

    new(30)

    def start_player_movement():
        player.animate_y(player.y+7, duration=0.3, curve=curve.out_sine)
        player.animate_rotation_z(player.rotation_z+180, duration=0.5, curve=curve.linear)

    def update():
        nonlocal score, is_game_over
        if is_game_over:
            return
        for ob in diam:
            ob.x-=20*time.dt
            if player.intersects(ob).hit:
                score+=3
                print(f"Score: {score}")
                diam.remove(ob)
                destroy(ob)
                score_text.text=f'Score: {score}'

        for ob in plates:
            ob.x-=20*time.dt

        for ob in obstacles:
            ob.x-=20*time.dt
            if player.intersects(ob).hit:
                print("You Lose!")
                destroy(player)
                show_game_over_message()
                is_game_over=True
                return

        if not player.intersects().hit:
            player.y-=25*time.dt
            player.y=max(-5, player.y)
            t=player.intersects()
            if t.hit:
                for en in t.entities:
                    if en.color==color.red:
                        print("You Lose!")
                        show_game_over_message()
                        is_game_over=True
                        return

        score+=1
        score_text.text=f'Score: {score}'

    def input(key):
        nonlocal is_game_over
        if key=="space":
            if player.intersects().hit:
                player.animate_y(player.y+7, duration=0.3, curve=curve.out_sine)
                player.animate_rotation_z(player.rotation_z+180, duration=0.5, curve=curve.linear)
                dust=Entity(model=Circle(), scale=-3, color=color.smoke, position=player.position)
                dust.animate_scale(2, duration=3, curve=curve.linear)
                dust.fade_out(duration=1)
        elif key=="r":
            if is_game_over:
                restart_game()
        elif key=="escape":
            exit_game()

    def restart_game():
        nonlocal score, is_game_over, game_over_text
        player.position=(0, 0, 0)
        player.y=0

        for entity in diam+plates+obstacles:
            destroy(entity)
        diam.clear()
        plates.clear()
        obstacles.clear()

        score=0
        score_text.text=f'Score: {score}'
        is_game_over=False

        if game_over_text:
            destroy(game_over_text)
            game_over_text=None

        new(30)
        start_player_movement()

    def exit_game():
        app.userExit()

    def show_game_over_message():
        nonlocal game_over_text
        game_over_text=Text(
            text="You lose!\nPress 'R' to restart the game or 'Escape' to exit.",
            origin=(0, 0),
            scale=2,
            color=color.white,
            position=(0, 0)
        )

    start_player_movement()

    app.run()

conn=sqlite3.connect('users.db')
cursor=conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
conn.commit()

def register_user():
    username=username_entry.get()
    password=password_entry.get()
    confirm_password=confirm_password_entry.get()

    if not username or not password or not confirm_password:
        messagebox.showwarning("Error", "All fields must be filled!")
    elif password != confirm_password:
        messagebox.showwarning("Error", "Passwords do not match!")
    else:
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", f"User {username} registered successfully!")
            main_window.after(100, lambda: main_window.destroy())
            start_game()
        except sqlite3.IntegrityError:
            messagebox.showwarning("Error", f"User {username} already exists!")

def login_user():
    username=username_entry.get()
    password=password_entry.get()

    cursor.execute("SELECT*FROM users WHERE username=? AND password=?", (username, password))
    user=cursor.fetchone()

    if user:
        messagebox.showinfo("Success", f"User {username} logged in successfully!")
        main_window.after(100, lambda: main_window.destroy())
        start_game()
    else:
        messagebox.showwarning("Error", "Incorrect username or password!")

main_window=tk.Tk()
main_window.title("Geometry Dash Login/Registration")
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

create_label("Login/Registration", "#ffcc00", "#000000", main_window, title_font, center=True)

create_label("Username:", "#00ff66", "#000000", main_window, label_font)
username_entry=tk.Entry(main_window, font=label_font, bg=entry_bg, fg=entry_fg)
username_entry.pack(pady=10, padx=50, fill='x')

create_label("Password:", "#31f2f5", "#000000", main_window, label_font)
password_entry=tk.Entry(main_window, show="*", font=label_font, bg=entry_bg, fg=entry_fg)
password_entry.pack(pady=10, padx=50, fill='x')

create_label("Confirm Password:", "#ff3333", "#000000", main_window, label_font)
confirm_password_entry=tk.Entry(main_window, show="*", font=label_font, bg=entry_bg, fg=entry_fg)
confirm_password_entry.pack(pady=10, padx=50, fill='x')

register_button=tk.Button(main_window, text="Register", font=(label_font[0], label_font[1], 'bold'), bg=button_bg, fg=button_fg, command=register_user, width=20, highlightbackground=outline_fg, highlightthickness=2)
register_button.pack(pady=10)

login_button=tk.Button(main_window, text="Login", font=(label_font[0], label_font[1], 'bold'), bg=button_bg, fg=button_fg, command=login_user, width=20, highlightbackground=outline_fg, highlightthickness=2)
login_button.pack(pady=10)

main_window.mainloop()

conn.close()
