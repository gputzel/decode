import sys

#print sys.argv

#What to do with the alphabet?

file1 = sys.argv[1]
file2 = sys.argv[2]
outputfile = sys.argv[3]

with open(file1,"rb") as file1:
    data1 = bytearray(file1.read())
    with open(file2,"rb") as file2:
        data2 = bytearray(file2.read())

#Truncate both the message and the key according to
#which of these is shorter
l = min(len(data1),len(data2))
data1 = data1[:l]
data2 = data2[:l]

output = bytearray(l)

for i in range(l):
    output[i] = data1[i] ^ data2[i]

with open(outputfile,"wb") as fout:
    fout.write(output)
