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
        return [db for db in r.json() if not db.startswith("_")]


def replicate(db, src, dst):
    headers = { "Content-Type": "application/json" }
    data = {
        "source": "{0}/{1}".format(src, db),
        "target": "{0}/{1}".format(dst, db),
        "create_target": True
    }

    r = requests.post("{0}/_replicate".format(src), json.dumps(data), headers=headers).json()

    if "error" in r:
        print("{0}: {1}".format(r["error"], r["reason"]))
    else:
        print("{0} has been replicated".format(db))

    
parser = argparse.ArgumentParser(description="back up couch databases, default back up all databases except for _replicator and _users, please note that this robot always do pull replication from destination host, so make sure both source and destination urls make sense for backup, e.g. if you are currently on host 192.168.133.129, you want to backup databases from http://localhost:5984 to http://192.168.133.128:5984, you might run backup_couch.py http://127.0.0.1:5984 http://192.168.133.128:5984, but this won't work as expected! Because this robot always run pull operation on destination host, so 127.0.0.1 is same machine as 192.168.133.128. To work correctly, use backup_couch.py http://192.168.133.129:5984 http://192.168.133.128:5984 for this situation")
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
