import sys
import argparse
from couch_lib import get_databases, replicate


parser = argparse.ArgumentParser(description="back up couch databases, default back up all databases except for _replicator and _users")
parser.add_argument("-b", "--databases", nargs="+", help="the databases to be backed up")
parser.add_argument("-p", "--push", help="push (from source), by default using pull (from destination)", action="store_true")
parser.add_argument("source", help="source couchdb url, specify credentials if authentication is required, e.g http://admin:123@127.0.0.1:5984")
parser.add_argument("destination", help="destination couchdb url, specify credentials if authentication is required, e.g http://admin:123@127.0.0.1:5984")

args = parser.parse_args()
src = args.source
dst = args.destination
dbs = args.databases or get_databases(src)
push = args.push

print("The following databases will be replicated from {0} to {1}:".format(src, dst))
print(" ".join(dbs))
answer = input("Do you want to continue? [y/N] ")

if answer == "y" or answer == "Y":
    for db in dbs:
        try:
            replicate(db, src, dst, push)
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print()
            sys.exit(1)
else:
    sys.exit(0)
