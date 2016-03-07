import time
import sys

epoch = int(sys.argv[1])

s, ms = divmod(epoch, 1000)

dtStr = "{}.{:03d}Z".format(time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(s)), ms)

print(dtStr)
