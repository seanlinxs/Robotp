import sys
import json
import requests
import argparse


def get_databases(url):
    try:
        r = requests.get("{0}/_all_dbs".format(url)).json()
    except Exception as e:
        print(e)
        sys.exit(1)

    if "error" in r:
        print("{0}: {1}".format(r["error"], r["reason"]))
        sys.exit(0)
    else:
        return [db for db in r if not db.startswith("_")]


def delete_database(db, url):
    headers = { "Content-Type": "application/json" }
    r = requests.delete("{0}/{1}".format(url, db), headers=headers).json()

    if "error" in r:
        print("{0}: {1}".format(r["error"], r["reason"]))
    else:
        print("{0} has been deleted".format(db))


def get_replications(url):
    r = requests.get("{0}/_replicator/_all_docs?include_docs=true".format(url)).json()

    if "error" in r:
        print("{0}: {1}".format(r["error"], r["reason"]))
        sys.exit(0)
    else:
        return r["rows"]


def delete_replication(replication, url):
    rid = replication["id"]
    rev = replication["value"]["rev"]
    request_url = "{0}/_replicator/{1}?rev={2}".format(url, rid, rev)
    r = requests.delete(request_url).json()

    if "error" in r:
        print("{0}: {1}".format(r["error"], r["reason"]))
    else:
        print("{0} has been deleted".format(rid))

    
parser = argparse.ArgumentParser(description="delete couch databases, default delete all databases except for _replicator and _user")
parser.add_argument("-b", "--databases", nargs="+", help="the databases to be backed up")
parser.add_argument("couch_url", help="couchdb url, specify credentials if authentication is required, e.g http://admin:123@127.0.0.1:5984")
args = parser.parse_args()
couch_url = args.couch_url
dbs = args.databases or get_databases(couch_url)
replications = [r for r in get_replications(couch_url) if not r["id"].startswith("_")]
replication_ids = [r["id"] for r in replications]

print("The following replications will be deleted:\n", " ".join(replication_ids))
print("The following databases will be deleted:\n", " ".join(dbs))

answer = input("Do you want to continue? [y/N] ")

if answer == 'y' or answer == 'Y':
    print("Delete replications:")
    for rep in replications:
        delete_replication(rep, couch_url)
        
    print("Delete databases:")
    for db in dbs:
        delete_database(db, couch_url)
elif answer == 'n' or answer == 'N':
    sys.exit(0)
