import sys
import argparse
from couch_lib import live_replicate, get_all_databases


parser = argparse.ArgumentParser(description="Create live replications from source to target server")
parser.add_argument("source", help="source couchdb url, specify credentials if authentication is required, e.g http://admin:123@127.0.0.1:5984")
parser.add_argument("target", help="target couchdb url, specify credentials if authentication is required, e.g http://admin:123@127.0.0.1:5984")
parser.add_argument("-b", "--databases", nargs="+", help="the databases, if not specified will do all databases, include _users and _replicator")

args = parser.parse_args()
source = args.source
target = args.target
dbs = args.databases

if dbs == None:
    try:
        dbs = get_all_databases(source)
    except Exception as e:
        print(e)
        sys.exit(-1)
        
print("The following databases will be live copied from {0} to {1}:".format(source, target))
print(" ".join(dbs))
answer = input("Do you want to continue? [y/N] ")

if answer == "y" or answer == "Y":
    for db in dbs:
        try:
            live_replicate(db, source, target)
            print("{0} copied".format(db))
        except Exception as e:
            print(e)
            sys.exit(-1)
        except KeyboardInterrupt:
            print()
            sys.exit(-1)

sys.exit(0)
