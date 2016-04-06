import sys
import time
import argparse
import pycouchdb
from urllib.parse import urlparse


parser = argparse.ArgumentParser(description="continuously replicate database(s)")
parser.add_argument("source", help="source couchdb server base_url, can contain auth data like: http://admin:123456@localhost:5984")
parser.add_argument("destination", help="destination couchdb server base_url, can contain auth data like: http://admin:123456@localhost:5984")
parser.add_argument("-d", "--databases", nargs="+", help="databases to be replicated, all databases if not specified")
parser.add_argument("-y", "--assumeyes", help="assume that the answer to any question which would be asked is yes", action="store_true")

args = parser.parse_args()
src = args.source
src_parsed_url = urlparse(src)
src_host = "{0}://{1}{2}".format(src_parsed_url.scheme, src_parsed_url.hostname, ":{0}".format(src_parsed_url.port) if src_parsed_url.port != None else "")
dst = args.destination
dst_parsed_url = urlparse(dst)
dst_host = "{0}://{1}{2}".format(dst_parsed_url.scheme, dst_parsed_url.hostname, ":{0}".format(dst_parsed_url.port) if dst_parsed_url.port != None else "")
dbs = args.databases
assumeyes = args.assumeyes

# server checking
try:
    src_server = pycouchdb.Server(src)
    src_info = src_server.info()
except Exception as e:
    print("Connect to {0} failed: {1}".format(src_host, e))
    sys.exit(-1)

try:
    dst_server = pycouchdb.Server(dst)
    dst_info = dst_server.info()
except Exception as e:
    print("Connect to {0} failed: {1}".format(dst_host, e))
    sys.exit(-1)

if dbs == None:
    dbs = [db for db in src_server]
    # replicate _replicator last until all db are ready
    dbs.remove("_replicator")
    dbs.append("_replicator")
        
# default No
answer = "n"

if not assumeyes:
    print("The following databases will be replicated from {0} to {1}:".format(src_host, dst_host))
    print(" ".join(dbs))
    answer = input("Do you want to continue? [y/N] ")

if assumeyes or answer == "y" or answer == "Y":
    for db in dbs:
        try:
            src_server.replicate("{0}/{1}".format(src, db), "{0}/{1}".format(dst, db), continuous=True, create_target=True)
            print(db)
        except Exception as e:
            print(e)
            sys.exit(-1)
