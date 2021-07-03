#!/usr/bin/env python3

import csv
from datetime import datetime


member_fields = [
    ['firstName', 'First Name'],
    ['lastName', 'Last Name'],
    ['dob', 'DOB'],
    ['address', 'Address'],
    ['postcode', 'Postcode'],
    ['emergencyContact', 'Emergency Contact'],
    ['emergencyNumber', 'Emergency Number'],
    ['ethnicity', 'Ethnicity'],
    ['gender', 'Gender'],
    ['language', 'Language'],
    ['religion', 'Religion'],
    ['school', 'School'],
    ['medical', 'Medical'],
    ['diet', 'Dietary'],
]


def write_attendance_csv(data):
    try:
        csv_file = open("attendances.csv", "w", newline="")
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow(["DateTime", "Name", "DOB", "Address"])
        for session in data:
            for record in data[session]:
                csv_writer.writerow([
                    session, 
                    record["name"], 
                    record["dob"], 
                    record["address"]
                ])
        csv_file.close()
        return 1
    except:
        return 0

def format_dob(dob):
    return f'{str(dob)[8:10]}/{str(dob)[5:7]}/{str(dob)[:4]}'

def write_members_csv(data):
    try:
        csv_file = open("members.csv", "w", newline="")
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow(["First Name", "Last Name", "DOB", "Address", "Postcode",
        "Emergency Contact", "Emergency Number", "Ethnicity", "Gender", "Language",
        "Religion", "School", "Medical", "Dietary"])
        for record in data:
            if 'medical' not in record:
                record['medical'] = ''
            if 'diet' not in record:
                record['diet'] = ''

            dob = format_dob(record['dob'])
            csv_writer.writerow([
                record['firstName'],
                record['lastName'],
                dob,
                record['address'],
                record['postcode'],
                record['emergencyContact'],
                f"'{record['emergencyNumber']}",
                record['ethnicity'],
                record['gender'],
                record['language'],
                record['religion'],
                record['school'],
                record['medical'],
                record['diet']
            ])
        csv_file.close()
        return 1
    except:
        return 0

def write_members_html(data):
    try:
        html_file = open("members.html", "w")
        html_file.write('<h1>Members</h1>\n')
        for record in data:
            html_file.write('<p>')
            for field in member_fields:
                if field[0] in record:
                    html_file.write(f"<strong>{field[1]}</strong> \t{record[field[0]]}<br>\n")
            html_file.write('</p>\n')
        html_file.close()
        return 1
    except:
        return 0
    


def write_attendance_html(data):
    try:
        html_file = open("attendances.html", "w")
        for session in data:
            html_file.write(f"<h2>{session}</h2>\n")
            for record in data[session]:
                html_file.write(f"<p><strong>{record['name']}</strong>\t{record['dob']}<br>{record['address']}</p>\n")
        html_file.close()
        return 1
    except:
        return 0


"""
result = db.all_attendances()
    for i in result:
        print(f"{i}\n{result[i]}")

>>>>

2021-05-27_23:00
[
    {'name': 'Simon Niall', 'dob': '20/02/2015', 'address': '101 Green Road S6 8DB'}, 
    {'name': 'Jessica Niall', 'dob': '22/11/2015', 'address': '496 Atlee Drive SW15 2OE'}, 
    {'name': 'Phillip Howell', 'dob': '03/08/2007', 'address': '404 Mile Green E17 7MA'}, 
    {'name': 'Phillip Donnell', 'dob': '08/04/2008', 'address': '363 Badgers Green SW14 5JF'}, 
    ...
]
2021-06-28_15:00
[
    {'name': 'Simon Niall', 'dob': '20/02/2015', 'address': '101 Green Road S6 8DB'}, 
    {'name': 'Chris Donnell', 'dob': '18/10/2012', 'address': '462 Badgers Road S18 5RR'}
]
2021-06-30_13:00
[
    {'name': 'Simon Niall', 'dob': '20/02/2015', 'address': '101 Green Road S6 8DB'}, 
    {'name': 'Jessica Niall', 'dob': '22/11/2015', 'address': '496 Atlee Drive SW15 2OE'}, 
    {'name': 'Sarah Tanner', 'dob': '18/05/2008', 'address': '158 Kimberly Green E9 3ZA'}, 
    {'name': 'Abbey Simmons', 'dob': '07/10/2010', 'address': '40 Badgers Green W13 1CS'}, 
    ...
]
"""
