import sys


for line in open(sys.argv[1]):
    for c in line:
        print(ord(c), end=" ")

