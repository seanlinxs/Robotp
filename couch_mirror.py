import sys
import argparse
from couch_lib import mirror


parser = argparse.ArgumentParser(description="Mirror couch databases, which create bidirectional live replication for specified databases between node1 and node2, any missed database will be created implicitly, i.e. if node1 has 1, 3, 5, 7, node2 has 2, 4, 6, 8, after mirror, both will have 1, 2, 3, 4, 5, 6, 7, 8")
parser.add_argument("node1", help="node1 couchdb url, specify credentials if authentication is required, e.g http://admin:123@127.0.0.1:5984")
parser.add_argument("node2", help="node2 couchdb url, specify credentials if authentication is required, e.g http://admin:123@127.0.0.1:5984")
parser.add_argument("-b", "--databases", nargs="+", help="the databases to be mirrored", required=True)

args = parser.parse_args()
node1 = args.node1
node2 = args.node2
dbs = args.databases

print("The following databases will be mirrored between {0} and {1}:".format(node1, node2))
print(" ".join(dbs))
answer = input("Do you want to continue? [y/N] ")

if answer == "y" or answer == "Y":
    for db in dbs:
        try:
            mirror(db, node1, node2)
        except Exception as e:
            print(e)
            sys.exit(-1)
        except KeyboardInterrupt:
            print()
            sys.exit(-1)

sys.exit(0)
