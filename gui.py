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
    button_state('disabled')
    global start_cal, end_cal, confirm_button, start_label, end_label, cancel_button
    now = datetime.now()
    start_cal = Calendar(
        root,
        font=("DejaVu Sans", 11),
        selectmode="day",
        year=now.year,
        month=now.month,
        day=now.day,
    )
    start_cal.grid(row=5, column=1, columnspan=3)
    start_label = Label(root, text="From")
    start_label.grid(row=4, column=1, columnspan=3, pady=5)
    end_cal = Calendar(
        root,
        font=("DejaVu Sans", 11),
        selectmode="day",
        year=now.year,
        month=now.month,
        day=now.day,
    )
    end_cal.grid(row=7, column=1, columnspan=3)
    end_label = Label(root, text="Until")
    end_label.grid(row=6, column=1, columnspan=3, pady=5)
    confirm_button = Button(
        root, text="Get Data", width=15, height=2, command=specified_dates
    )
    cancel_button = Button(root, text="Cancel", width=15, height=2, command=cancel_datepicker)
    confirm_button.grid(row=8, column=3, padx=25, pady=14)
    cancel_button.grid(row=8, column=1, padx=25, pady=14)

def cancel_datepicker():
    close_datepicker()
    button_state('normal')
    

def close_datepicker():
    start_cal.destroy()
    end_cal.destroy()
    start_label.destroy()
    end_label.destroy()
    confirm_button.destroy()
    cancel_button.destroy()


def button_state(state):
    since_last_button.config(state=state)
    specify_dates_button.config(state=state)
    all_data_button.config(state=state)


def write_and_feedback(attendance_data, member_data):
    if file_export.write_attendance_csv(attendance_data):
        attendance_csv_feedback = "Atendance Sheet Created!"
    else:
        attendance_csv_feedback = (
            "Error: file_export.write_attendance_csv(attendance_data)"
        )
    attendance_csv_label = Label(root, text=attendance_csv_feedback)
    attendance_csv_label.grid(row=6, column=1, columnspan=3, pady=10)

    if file_export.write_attendance_html(attendance_data):
        attendance_html_feedback = "Attendance Page Created!"
    else:
        attendance_html_feedback = (
            "Error: file_export.write_attendance_html(attendance_data)"
        )
    attendance_html_label = Label(root, text=attendance_html_feedback)
    attendance_html_label.grid(row=7, column=1, columnspan=3, pady=10)

    if file_export.write_members_csv(member_data):
        member_csv_feedback = "Members Sheet Created!"
    else:
        member_csv_feedback = "Error: file_export.write_members_csv(member_data)"
    member_csv_label = Label(root, text=member_csv_feedback)
    member_csv_label.grid(row=8, column=1, columnspan=3, pady=10)

    if file_export.write_members_html(member_data):
        member_html_feedback = "Members Page Created!"
    else:
        member_html_feedback = "Error: file.export.write_members_html(member_data)"
    member_html_label = Label(root, text=member_html_feedback)
    member_html_label.grid(row=9, column=1, columnspan=3, pady=10)


def log_dump(dump_type):
    dump_id = db.record_dump(dump_type, datetime.now())
    if dump_id:
        dump_feedback = f"Dump Recorded: {dump_id}!"
    else:
        dump_feedback = "Error: db.record_dump"
    dump_display = Label(root, text=dump_feedback)
    dump_display.grid(row=10, column=1, columnspan=3)


def fetch_all():
    button_state('disabled')

    attendance_data = db.get_atendance_data({})
    member_data = db.get_member_data({})

    write_and_feedback(attendance_data, member_data)
    log_dump("all")


def since_last_dump():
    button_state('disabled')
    last_dump = db.get_last_dump()
    if last_dump:
        dump_date = datetime(
            int(last_dump.strftime("%Y")),
            int(last_dump.strftime("%m")),
            int(last_dump.strftime("%d")),
        )
        attendance_query = {"datetime": {"$gte": dump_date}}
        members_query = {"dateJoined": {"$gte": dump_date}}
        attendance_data = db.get_atendance_data(attendance_query)
        member_data = db.get_member_data(members_query)
    else:
        attendance_data = db.get_atendance_data({})
        member_data = db.get_member_data({})

    write_and_feedback(attendance_data, member_data)
    log_dump("next")


def specified_dates():
    # get date
    start_string = start_cal.get_date()
    finish_string = end_cal.get_date()

    close_datepicker()
    # format date
    start_iso = datetime(
        int(start_string[-4:]), int(start_string[3:5]), int(start_string[:2])
    )
    finish_iso = datetime(
        int(finish_string[-4:]), int(finish_string[3:5]), int(finish_string[:2]), 23, 59
    )

    attendance_query = {"datetime": {"$gte": start_iso, "$lte": finish_iso}}
    member_query = {"dateJoined": {"$gte": start_iso, "$lte": finish_iso}}
    attendance_data = db.get_atendance_data(attendance_query)
    member_data = db.get_member_data(member_query)

    write_and_feedback(attendance_data, member_data)
    log_dump("date")


since_last_button = Button(
    root, text="Since Last Dump", width=15, height=2, command=since_last_dump
)
since_last_button.grid(row=3, column=1, padx=25, pady=14)

specify_dates_button = Button(
    root, text="Specify Dates", width=15, height=2, command=show_datepickers
)
specify_dates_button.grid(row=3, column=2, padx=25, pady=14)

all_data_button = Button(
    root, text="All Data (Slow!)", width=15, height=2, command=fetch_all
)
all_data_button.grid(row=3, column=3, padx=25, pady=14)

root.mainloop()
