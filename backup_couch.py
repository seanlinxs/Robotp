import sys
import json
import requests
import argparse


def get_databases(url):
    r = requests.get("{0}/_all_dbs".format(url))

    if "error" in r:
        print("{0}: {1}".format(r["error"], r["reason"]))
        sys.exit(0)
    else:
        return [db for db in req.json() if not db.startswith("_")]


def replicate(db, src, dst):
    headers = { "Content-Type": "application/json" }
    data = {
        "source": "{0}/{1}".format(src, db),
        "target": "{0}/{1}".format(dst, db),
        "create_target": True
    }

    r = requests.post("{0}/_replicate".format(dst), json.dumps(data), headers=headers).json()

    if "error" in r:
        print("{0}: {1}".format(r["error"], r["reason"]))
    else:
        print("{0} has been replicated".format(db))

    
parser = argparse.ArgumentParser(description="back up couch databases, default back up all databases except for _replicator and _user")
parser.add_argument("-b", "--databases", nargs="+", help="the databases to be backed up")
parser.add_argument("source", help="source couchdb url, specify credentials if authentication is required, e.g http://admin:123@127.0.0.1:5984")
parser.add_argument("destination", help="destination couchdb url, specify credentials if authentication is required, e.g http://admin:123@127.0.0.1:5984")

args = parser.parse_args()

src = args.source
dst = args.destination

dbs = args.databases or get_databases(src)

print("The following databases will be replicated from {0} to {1}:\n{2}\n".format(src, dst, " ".join(dbs)))
answer = input("Do you want to continue? [y/N] ")

if answer == "y" or answer == "Y":
    for db in dbs:
        try:
            replicate(db, src, dst)
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print()
            sys.exit(1)
elif answer == "n" or answer == "N":
    sys.exit(0)
