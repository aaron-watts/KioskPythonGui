#!/usr/bin/env python3

from pymongo import MongoClient
from bson.objectid import ObjectId
import pprint

client = MongoClient("mongodb://localhost:27017/")
db = client.registerApp
members_collection = db.members
attendances_collection = db.attendances
dumps_collection = db.dumps

# IDs must be formatted with bson.objectId to yield results
# any_id = ObjectId(attendances_collection.find_one({})['member'])
# print(members_collection.find_one({"_id": any_id})["firstName"])

def get_data(query):
    attendance_records = {}
    for attendance in attendances_collection.find(query):
        # populate members
        member_id = ObjectId(attendance["member"])
        member = members_collection.find_one({"_id": member_id})
        name = f'{member["firstName"]} {member["lastName"]}'
        dob = f'{str(member["dob"])[8:10]}/{str(member["dob"])[5:7]}/{str(member["dob"])[:4]}'
        address = f'{member["address"]} {member["postcode"]}'
        # create dictionary keys using datetime
        date_attended = str(attendance["datetime"])
        this_key = f"{date_attended[:4]}-{date_attended[5:7]}-{date_attended[8:10]}_{date_attended[11:13]}:00"
        if this_key not in attendance_records:
            attendance_records[this_key] = []
        # append members to dictionary list
        attendance_records[this_key].append(
            {"name": name, "dob": dob, "address": address}
        )
    return attendance_records
    
# Add dump to database
def record_dump(dump_type, dump_date):
    try:
        new_dump = {
            "dumpType": dump_type,
            "dumpDate": dump_date
        }
        dump_id = dumps_collection.insert_one(new_dump).inserted_id
        print(dump_id)
        return dump_id
    except:
        return 0

def get_last_dump():
    dump_list = []
    dumps = dumps_collection.find({"dumpType":"next"}).sort("dumpDate")
    for dump in dumps:
        dump_list.append(dump)
    if not len(dump_list):
        return 0
    return dump_list[-1]['dumpDate']