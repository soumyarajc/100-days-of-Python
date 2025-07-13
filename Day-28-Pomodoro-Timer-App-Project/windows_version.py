import tkinter
from tkinter import *
import math
import pygame
import threading
from plyer import notification

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
is_paused = False
time_left = 0

# Initialize pygame mixer
pygame.mixer.init()

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps, is_paused, time_left
    if timer:
        window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title.config(text="Timer")
    checks.config(text="")
    reps = 0
    is_paused = False
    time_left = 0
    pause_button.config(text="Pause")
    pygame.mixer.music.stop()

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps, is_paused
    if is_paused:
        is_paused = False
        count_down(time_left)
    else:
        reps += 1
        work_sec = WORK_MIN * 60
        short_break_sec = SHORT_BREAK_MIN * 60
        long_break_sec = LONG_BREAK_MIN * 60

        if reps % 8 == 0:
            count_down(long_break_sec)
            title.config(text="Break", fg=RED)
            threading.Thread(target=play_sound_for_duration, args=(LONG_BREAK_MIN,)).start()
        elif reps % 2 == 0:
            count_down(short_break_sec)
            title.config(text="Break", fg=PINK)
            threading.Thread(target=play_sound_for_duration, args=(SHORT_BREAK_MIN,)).start()
        else:
            count_down(work_sec)
            title.config(text="Work", fg=GREEN)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global timer, time_left
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        time_left = count
        timer = window.after(1000, count_down, count - 1)
    else:
        if reps % 2 == 0:
            show_break_notification("Break Over", None)
        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        checks.config(text=marks)

# ---------------------------- PAUSE MECHANISM ------------------------------- #
def pause_timer(event=None):
    global is_paused
    if is_paused:
        is_paused = False
        pause_button.config(text="Pause")
        count_down(time_left)
    else:
        window.after_cancel(timer)
        is_paused = True
        pause_button.config(text="Unpause")

# ---------------------------- BREAK NOTIFICATION ------------------------------- #
def show_break_notification(title, break_min):
    if break_min is None:
        message = "Time to get back to work!"
    else:
        message = f"Time for a {break_min}-minute break!"

    notification.notify(
        title=title,
        message=message,
        timeout=10
    )

def play_sound_for_duration(duration_min):
    pygame.mixer.music.load("/mnt/data/acoustic_guitar.wav")
    pygame.mixer.music.play(loops=-1)
    threading.Event().wait(duration_min * 60)
    pygame.mixer.music.stop()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro Timer")
window.config(padx=50, pady=30, bg=YELLOW)  # Reduced padding

title = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 40))  # Smaller font
title.grid(column=1, row=0)

canvas = Canvas(width=150, height=180, bg=YELLOW, highlightthickness=0)  # Smaller canvas
Tomato = PhotoImage(file="tomato_resized.png")  # Use resized image
canvas.create_image(75, 90, image=Tomato)  # Adjusted image position
timer_text = canvas.create_text(75, 110, text="00:00", fill="white", font=(FONT_NAME, 30, "bold"))  # Smaller font
canvas.grid(column=1, row=1)

start_button = Button(text="Start", highlightthickness=0, bg=YELLOW, activebackground=YELLOW, relief=FLAT, command=start_timer, font=(FONT_NAME, 10))  # Smaller font
start_button.grid(column=0, row=2, pady=(20, 0))  # Added padding

pause_button = Button(text="Pause", highlightthickness=0, bg=YELLOW, activebackground=YELLOW, relief=FLAT, font=(FONT_NAME, 10))  # Smaller font
pause_button.grid(column=1, row=2, pady=(20, 0))  # Added padding
pause_button.bind('<Button-1>', pause_timer)  # Use single click

reset_button = Button(text="Reset", highlightthickness=0, bg=YELLOW, activebackground=YELLOW, relief=FLAT, command=reset_timer, font=(FONT_NAME, 10))  # Smaller font
reset_button.grid(column=2, row=2, pady=(20, 0))  # Added padding

checks = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 12))  # Smaller font
checks.grid(column=1, row=3)

window.mainloop()
