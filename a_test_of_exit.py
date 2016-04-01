import sys


try:
    raise Exception("a test of sys.exit in try except")
except Exception as e:
    print(e)
    sys.exit(-1)
