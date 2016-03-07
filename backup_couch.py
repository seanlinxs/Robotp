import sys
import json
import requests
import argparse


def get_databases(url):
    req = requests.get("{0}/_all_dbs".format(url))
    return req.json()

parser = argparse.ArgumentParser(description="back up couch databases, default back up all databases except for _replicator and _user")
parser.add_argument("-b", "--databases", metavar="db", nargs="+", help="the databases to be backed up")
parser.add_argument("source", help="source couchdb url, specify credentials if authentication is required, e.g http://admin:123@127.0.0.1:5984")
parser.add_argument("destination", help="destination couchdb url, specify credentials if authentication is required, e.g http://admin:123@127.0.0.1:5984")

args = parser.parse_args()

src = args.source
dst = args.destination

dbs = args.databases or get_databases(src, args.susername, args.spassword)

print(dbs)

sys.exit(0)
