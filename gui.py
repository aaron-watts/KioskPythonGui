#!/usr/bin/env python3

from tkinter import *
from tkcalendar import *
from datetime import datetime
import db_utils as db
import f_utils as file_export

root = Tk()
root.title("Data Dump")
root.geometry("600x600")


def show_datepickers():
    global start_cal, end_cal, confirm_button, start_label, end_label
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
    confirm_button = Button(root, text="Get Data", width=15, command=specified_dates)
    confirm_button.grid(row=6, column=2, padx=25)

def close_datepicker():
    start_cal.destroy()
    end_cal.destroy()
    start_label.destroy()
    end_label.destroy()
    confirm_button.destroy()

def feedback(data):
    if file_export.write_to_csv(data):
        csv_feedback = "Atendance Sheet Created!"
    else:
        csv_feedback = "Error: file_export.write_to_csv(data)"
    csv_display = Label(root, text=csv_feedback)
    csv_display.grid(row=6, column=1, columnspan=3)
    
    if file_export.write_to_html(data):
        html_feedback = "Attendance Page Created!"
    else:
        html_feedback = "Error: file_export.write_to_html"
    html_display = Label(root, text=html_feedback)
    html_display.grid(row=7, column=1, columnspan=3)


def log_dump(dump_type):
    dump_id = db.record_dump(dump_type, datetime.now())
    if dump_id:
        dump_feedback = f"Dump Recorded: {dump_id}!"
    else:
        dump_feedback = "Error: db.record_dump"
    dump_display = Label(root, text=dump_feedback)
    dump_display.grid(row=8, column=1, columnspan=3)


def fetch_all():
    data = db.all_attendances()
    feedback(data)
    log_dump("all")


def since_last_dump():
    pass


def specified_dates():
    #get date
    start_string = start_cal.get_date()
    finish_string = end_cal.get_date()
    
    close_datepicker()
    #format date
    start_iso = datetime(int(start_string[-4:]), int(start_string[3:5]), int(start_string[:2]))
    finish_iso = datetime(int(finish_string[-4:]), int(finish_string[3:5]), int(finish_string[:2]), 23, 59)

    data = db.specified_dates(start_iso, finish_iso)
    feedback(data)
    log_dump("date")


instruction = Label(root, text="Please Select:")
instruction.grid(row=2, column=1, columnspan=3)

button1 = Button(root, text="Since Last Dump", width=15)
button1.grid(row=3, column=1, padx=25)

button2 = Button(root, text="Specify Dates", width=15, command=show_datepickers)
button2.grid(row=3, column=2, padx=25)

button3 = Button(root, text="All Data (Slow!)", width=15, command=fetch_all)
button3.grid(row=3, column=3, padx=25)

root.mainloop()
