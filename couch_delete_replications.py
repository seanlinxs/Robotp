import sys
import argparse
from couch_lib import delete, get_replications

    
parser = argparse.ArgumentParser(description="Delete couch replications, delete all by default")
parser.add_argument("base_url", help="couchdb base url, specify credentials if authentication is required, e.g http://admin:123@127.0.0.1:5984")
args = parser.parse_args()
base_url = args.base_url
replications = [r for r in get_replications(base_url) if r["id"] != "_design/_replicator"]
replication_ids = [r["id"] for r in replications]

if len(replication_ids) <= 0:
    print("No replications found")
    sys.exit(0)
    
print("The following replications will be deleted:")
print(" ".join(replication_ids))
answer = input("Do you want to continue? [y/N] ")

if answer == 'y' or answer == 'Y':
    for r in replications:
        delete(base_url, "_replicator", r["id"], r["value"]["rev"])
else:
    sys.exit(0)
