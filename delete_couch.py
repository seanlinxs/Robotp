import sys
import argparse
from couch_lib import get_databases, delete_database


parser = argparse.ArgumentParser(description="Delete couch databases, default delete all databases except for _replicator and _user")
parser.add_argument("-b", "--databases", nargs="+", help="the databases to be deleted")
parser.add_argument("base_url", help="couchdb base url, specify credentials if authentication is required, e.g http://admin:123@127.0.0.1:5984")
args = parser.parse_args()
base_url = args.base_url
dbs = args.databases or get_databases(base_url)

print("The following databases will be deleted, make sure back up first if needed:")
print(" ".join(dbs))
answer = input("Do you want to continue? [y/N] ")

if answer == 'y' or answer == 'Y':
    for db in dbs:
        delete_database(base_url, db)
else:
    sys.exit(0)
