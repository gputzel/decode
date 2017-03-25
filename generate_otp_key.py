import sys
import os

n = int(sys.argv[1])
filename = sys.argv[2]

key = bytearray(os.urandom(n))

with open(filename,"wb") as fout:
    fout.write(key)
