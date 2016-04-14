import sys
import argparse
from couchdb_lib import get_server, mask_passwd


parser = argparse.ArgumentParser(description="replicate database(s)")
parser.add_argument("source", help="source couchdb server base_url, can contain auth data like: http://admin:123456@localhost:5984")
parser.add_argument("destination", help="destination couchdb server base_url, can contain auth data like: http://admin:123456@localhost:5984")
parser.add_argument("-d", "--databases", nargs="+", help="databases to be replicated, all databases if not specified")
parser.add_argument("-y", "--assumeyes", help="assume that the answer to any question which would be asked is yes", action="store_true")
parser.add_argument("-p", "--usepull", help="use pull on destination, default use push on source", action="store_true")
parser.add_argument("-c", "--continuous", help="create continuous replication", action="store_true")

args = parser.parse_args()
src = args.source
dst = args.destination
dbs = args.databases
assumeyes = args.assumeyes
usepull = args.usepull
continuous = args.continuous

# server checking
src_server, src_error = get_server(src)
if src_server == None:
    print(src_error)
    sys.exit(-1)

dst_server, dst_error = get_server(dst)
if dst_server == None:
    print(dst_error)
    sys.exit(-1)

if dbs == None:
    dbs = [db for db in src_server]
    # replicate _replicator last until all db are ready
    dbs.remove("_replicator")
    dbs.append("_replicator")
        
# default No
answer = "n"

if not assumeyes:
    print("The following databases will be replicated from {0} to {1}:".format(mask_passwd(src), mask_passwd(dst)))
    print(" ".join(dbs))
    answer = input("Do you want to continue? [y/N] ")

if assumeyes or answer == "y" or answer == "Y":
    for db in dbs:
        try:
            if usepull:
                dst_server.replicate("{0}/{1}".format(src, db), "{0}/{1}".format(dst, db), continuous=continuous, create_target=True)
            else:
                src_server.replicate("{0}/{1}".format(src, db), "{0}/{1}".format(dst, db), continuous=continuous, create_target=True)
            print(db)
        except Exception as e:
            print("Failed: {0}".format(e))
            sys.exit(-1)
