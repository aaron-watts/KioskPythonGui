#!/usr/bin/env python3

from pymongo import MongoClient
from bson.objectid import ObjectId
import pprint

client = MongoClient("mongodb://localhost:27017/")
db = client.registerApp
members_collection = db.members
attendances_collection = db.attendances

# IDs must be formatted with bson.objectId to yield results
# any_id = ObjectId(attendances_collection.find_one({})['member'])
# print(members_collection.find_one({"_id": any_id})["firstName"])

# Loop through ALL attendances and collect associated member data
def all_attendances():
    attendance_records = {}
    for attendance in attendances_collection.find({}):
        member_id = ObjectId(attendance["member"])
        member = members_collection.find_one({"_id": member_id})
        date_attended = str(attendance["datetime"])
        this_key = f"{date_attended[:4]}-{date_attended[5:7]}-{date_attended[8:10]}_{date_attended[11:13]}:00"
        name = f'{member["firstName"]} {member["lastName"]}'
        dob = f'{str(member["dob"])[8:10]}/{str(member["dob"])[5:7]}/{str(member["dob"])[:4]}'
        address = f'{member["address"]} {member["postcode"]}'
        if this_key not in attendance_records:
            attendance_records[this_key] = []
        attendance_records[this_key].append(
            {"name": name, "dob": dob, "address": address}
        )
    return attendance_records
