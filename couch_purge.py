import sys
import argparse
import re
from couch_lib import purge


parser = argparse.ArgumentParser(description="Purge couch doc permernantly, not recoverable, not marked as deleted")
parser.add_argument("base_url", help="couchdb base url, specify credentials if authentication is required, e.g http://admin:123@127.0.0.1:5984")
parser.add_argument("database", help="couchdb database name")
parser.add_argument("doc_id", help="document id")
parser.add_argument("revs", help="comma delimited revsions")
args = parser.parse_args()
base_url = args.base_url
database = args.database
doc_id = args.doc_id
revs = re.compile(",\s*").split(args.revs)

print("{0} will be purged, you CAN NOT UNDO this action!".format(doc_id))
answer = input("Do you want to continue? [y/N] ")

if answer == 'y' or answer == 'Y':
    purge(base_url, database, doc_id, revs)
else:
    sys.exit(0)
