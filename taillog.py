import sys
import time

def tail(file):
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

f = open(sys.argv[1])
f.seek(0, 2)

try:
    for line in tail(f):
        print(line, end='')
except KeyboardInterrupt:
    sys.exit(0)
