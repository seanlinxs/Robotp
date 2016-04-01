import sys
import argparse
import pycouchdb
from urllib import urlparse


parser = argparse.ArgumentParser(description="live copy database(s)")
parser.add_argument("source", help="source couchdb server base_url, can contain auth data like this: http://admin:123456@localhost:5984")
parser.add_argument("destination", help="destination couchdb server base_url, can contain auth data like this: http://admin:123456@localhost:5984")
parser.add_argument("-d", "--databases", nargs="+", help="databases to be copied, all databases if not specified")

args = parser.parse_args()
src = args.source
src_parsed_url = urlparse(src)
src_host = "{0}"
dst = args.destination
dst_parsed_url = urlparse(dst)
dbs = args.databases

# server checking
try:
    src_server = pycouchdb.Server(source)
    src_info = src_server.info()
except Exception as e:
    print("Connect to server {0} failed: ".format(source, e))
    sys.exit(-1)

try:
    dst_server = pycouchdb.Server(destination)
    dst_info = src_server.info()
except Exception as e:
    print(e)
    sys.exit(-1)

if dbs == None:
    try:
        dbs = get_all_databases(source)
    except Exception as e:
        print(e)
        sys.exit(-1)
        
print("The following databases will be live copied from {0} to {1}:".format(source, destination))
print(" ".join(dbs))
answer = input("Do you want to continue? [y/N] ")

if answer == "y" or answer == "Y":
    for db in dbs:
        try:
            live_replicate(db, source, destination)
            print("{0} copied".format(db))
        except Exception as e:
            print(e)
            sys.exit(-1)
        except KeyboardInterrupt:
            print()
            sys.exit(-1)

sys.exit(0)
