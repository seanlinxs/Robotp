import sys

factor = 2
first = 5

def waitingtime(n):
    if n == 1:
        return first
    else:
        return waitingtime(n - 1) * factor

print(waitingtime(int(sys.argv[1])))
