import sys
import argparse
from couch_lib import purge, get_replications

    
parser = argparse.ArgumentParser(description="Purge couch replications, default delete all replications")
parser.add_argument("base_url", help="couchdb base url, specify credentials if authentication is required, e.g http://admin:123@127.0.0.1:5984")
args = parser.parse_args()
base_url = args.base_url
replications = [r for r in get_replications(base_url) if r["id"] != "_design/_replicator"]
replication_ids = [r["id"] for r in replications]

print("The following replications will be purged:")
print(" ".join(replication_ids))
answer = input("Do you want to continue? [y/N] ")

if answer == 'y' or answer == 'Y':
    for r in replications:
        purge(base_url, "_replicator", r["id"], [c["rev"] for c in r["changes"]])
else:
    sys.exit(0)
