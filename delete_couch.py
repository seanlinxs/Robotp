import sys
import json
import requests
import argparse


def get_databases(url):
    r = requests.get("{0}/_all_dbs".format(url))
    return [db for db in r.json() if not db.startswith("_")]


def delete_database(db, url):
    print("Deleting {0}".format(db))
    headers = { "Content-Type": "application/json" }
    r = requests.delete("{0}/{1}".format(url, db), headers=headers).json()

    if "error" in r:
        print("{0}: {1}".format(r["error"], r["reason"]))


def get_replications(url):
    r = requests.get("{0}/_replicator/_all_docs?include_docs=true".format(url)).json()
    return r["rows"]


def delete_replication(replication, url):
    rid = replication["id"]
    print("Deleteing {0}".format(rid))
    rev = replication["value"]["rev"]
    request_url = "{0}/_replicator/{1}?rev={2}".format(url, rid, rev)
    r = requests.delete(request_url).json()

    if "error" in r:
        print("{0}: {1}".format(r["error"], r["reason"]))

    
parser = argparse.ArgumentParser(description="delete couch databases, default delete all databases except for _replicator and _user")
parser.add_argument("-b", "--databases", nargs="+", help="the databases to be backed up")
parser.add_argument("couch_url", help="couchdb url, specify credentials if authentication is required, e.g http://admin:123@127.0.0.1:5984")
args = parser.parse_args()
couch_url = args.couch_url
dbs = args.databases or get_databases(couch_url)
replications = get_replications(couch_url)

answer = input("The following databases will be deleted from {0}:\n{1}\nDo you want to continue? [y/N] ".format(couch_url, ", ".join(dbs)))

if answer == 'y' or answer == 'Y':
    for rep in replications:
        if rep["id"].startswith("_"):
            continue
        delete_replication(rep, couch_url)
        
    for db in dbs:
        try:
            delete_database(db, couch_url)
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print()
            sys.exit(1)
elif answer == 'n' or answer == 'N':
    sys.exit(0)
