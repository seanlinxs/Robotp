import json
import requests


def purge(base_url, database, doc_id, revs):
    url = "{0}/{1}/_purge".format(base_url, database)
    data = { doc_id: revs }
    headers = { "Content-Type": "application/json" }
    r = requests.post(url, json.dumps(data), headers=headers).json()
    print(r)


def get_replications(base_url):
    r = requests.get("{0}/_replicator/_changes".format(base_url)).json()

    if "error" in r:
        print("{0}: {1}".format(r["error"], r["reason"]))
        sys.exit(0)
    else:
        return r["results"]

def get_databases(base_url):
    try:
        r = requests.get("{0}/_all_dbs".format(base_url)).json()
    except Exception as e:
        print(e)
        sys.exit(1)

    if "error" in r:
        print("{0}: {1}".format(r["error"], r["reason"]))
        sys.exit(0)
    else:
        return [db for db in r if not db.startswith("_")]


def delete_database(base_url, database):
    headers = { "Content-Type": "application/json" }
    r = requests.delete("{0}/{1}".format(base_url, database), headers=headers).json()

    if "error" in r:
        print("{0}: {1}".format(r["error"], r["reason"]))
    else:
        print("{0} has been deleted".format(database))


