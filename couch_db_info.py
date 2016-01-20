import requests
import sys
import json


if (len(sys.argv) != 4):
    print("Usage: {0} <couch_url> <username> <password>".format(sys.argv[0]))
    sys.exit(-1)
    
couch_base_url, couch_username, couch_password = sys.argv[1:]
r = requests.get("{0}/{1}".format(couch_base_url, "_all_dbs"), auth=(couch_username, couch_password))

dbs = r.json()

for db in dbs:
    info = requests.get("{0}/{1}".format(couch_base_url, db), auth=(couch_username, couch_password))
    print("{0}: {1}".format(db, info.json()))
