#!/usr/bin/env python3

from tkinter import *
from tkcalendar import *
from datetime import datetime
import db_utils as db

root = Tk()
root.title("Data Dump")
root.geometry("600x600")


def show_datepickers():
    now = datetime.now()
    start_cal = Calendar(
        root,
        font=("DejaVu Sans", 11),
        selectmode="day",
        year=now.year,
        month=now.month,
        day=now.day,
    )
    start_cal.grid(row=4, column=2, columnspan=2, sticky=W)
    start_label = Label(root, text="From:")
    start_label.grid(row=4, column=1, sticky=NE)
    end_cal = Calendar(
        root,
        font=("DejaVu Sans", 11),
        selectmode="day",
        year=now.year,
        month=now.month,
        day=now.day,
    )
    end_cal.grid(row=5, column=2, columnspan=2, sticky=W)
    end_label = Label(root, text="Until:")
    end_label.grid(row=5, column=1, sticky=NE)


def fetch_all():
    result = db.all_attendances()
    for i in result:
        print(f"{i}\n{result[i]}")


instruction = Label(root, text="Please Select:")
instruction.grid(row=2, column=1, columnspan=3)

button1 = Button(root, text="Since Last Dump", width=15)
button1.grid(row=3, column=1, padx=25)

button2 = Button(root, text="Specify Dates", width=15, command=show_datepickers)
button2.grid(row=3, column=2, padx=25)

button3 = Button(root, text="All Data (Slow!)", width=15, command=fetch_all)
button3.grid(row=3, column=3, padx=25)

root.mainloop()