import json
import requests


def delete(base_url, database, doc_id, rev):
    url = "{0}/{1}/{2}?rev={3}".format(base_url, database, doc_id, rev)
    r = requests.delete(url).json()
    print(r)


def purge(base_url, database, doc_id, revs):
    url = "{0}/{1}/_purge".format(base_url, database)
    data = { doc_id: revs }
    headers = { "Content-Type": "application/json" }
    r = requests.post(url, json.dumps(data), headers=headers).json()
    print(r)


def get_replications(base_url):
    r = requests.get("{0}/_replicator/_all_docs".format(base_url)).json()

    if "error" in r:
        print("{0}: {1}".format(r["error"], r["reason"]))
        sys.exit(0)
    else:
        return r["rows"]

def get_replication_changes(base_url):
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


def get_all_databases(base_url):
    try:
        r = requests.get("{0}/_all_dbs".format(base_url)).json()
    except Exception as e:
        print(e)
        sys.exit(1)

    if "error" in r:
        print("{0}: {1}".format(r["error"], r["reason"]))
        sys.exit(0)
    else:
        return r


def delete_database(base_url, database):
    headers = { "Content-Type": "application/json" }
    r = requests.delete("{0}/{1}".format(base_url, database), headers=headers).json()

    if "error" in r:
        print("{0}: {1}".format(r["error"], r["reason"]))
    else:
        print("{0} has been deleted".format(database))


def replicate(db, src, dst, push):
    headers = { "Content-Type": "application/json" }
    data = {
        "source": "{0}/{1}".format(src, db),
        "target": "{0}/{1}".format(dst, db),
        "create_target": True
    }

    r = requests.post("{0}/_replicate".format(src if push else dst), json.dumps(data), headers=headers).json()

    if "error" in r:
        print("{0}: {1}".format(r["error"], r["reason"]))
    else:
        print("{0} has been replicated".format(db))

def db_exists(base_url, db):
    r = requests.head("{0}/{1}".format(base_url, db))

    return r.status_code == 200

def live_replicate(db, src, dst):
    headers = { "Content-Type": "application/json" }
    data = {
        "source": "{0}/{1}".format(src, db),
        "target": "{0}/{1}".format(dst, db),
        "create_target": True,
        "continuous": True
    }

    r = requests.post("{0}/_replicate".format(src), json.dumps(data), headers=headers).json()

    if "error" in r:
        raise Exception(("{0}: {1}".format(r["error"], r["reason"])))

        
def mirror(db, node1, node2):
    db_exists_in_node1 = db_exists(node1, db)
    db_exists_in_node2 = db_exists(node2, db)

    if not db_exists_in_node1 and not db_exists_in_node2:
        print("Cannot mirror, {0} not found".format(db))
        return
        
    try:
        if db_exists_in_node1:
            live_replicate(db, node1, node2)
            live_replicate(db, node2, node1)
        else:
            live_replicate(db, node2, node1)
            live_replicate(db, node1, node2)
        print("Live replications {0}/{1} <-> {2}/{1} have been created".format(node1, db, node2))
    except Exception as e:
        print(e)


def cancel_live_replicate(db, src, dst):
    headers = { "Content-Type": "application/json" }
    data = {
        "source": "{0}/{1}".format(src, db),
        "target": "{0}/{1}".format(dst, db),
        "create_target": True,
        "continuous": True,
        "cancel": True
    }

    r = requests.post("{0}/_replicate".format(src), json.dumps(data), headers=headers).json()

    if "error" in r:
        raise Exception(("{0}: {1}".format(r["error"], r["reason"])))

        
def cancel_mirror(db, node1, node2):
    db_exists_in_node1 = db_exists(node1, db)
    db_exists_in_node2 = db_exists(node2, db)

    if not db_exists_in_node1 and not db_exists_in_node2:
        print("Cannot cancel mirror, {0} not found".format(db))
        return
        
    try:
        if db_exists_in_node1:
            cancel_live_replicate(db, node1, node2)
            cancel_live_replicate(db, node2, node1)
        else:
            cancel_live_replicate(db, node2, node1)
            cancel_live_replicate(db, node1, node2)
        print("Live replications {0}/{1} <-> {2}/{1} have been canceled".format(node1, db, node2))
    except Exception as e:
        print(e)
