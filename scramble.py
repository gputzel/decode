import sys,string
import random

#scramble.py
#A simple tool for scrambling a given plaintext
#Usage: python scramble.py plaintext.txt > output.txt

def scramble(text):
	alphabet=list(set(text))
	#Make a random permutation from the alphabet to itself
	perm={}
	for c in alphabet:
		perm[c]=c
	for i in range(1,len(alphabet)):
		j = random.randint(0,i-1)
		temp=perm[alphabet[i]]
		perm[alphabet[i]]=perm[alphabet[j]]
		perm[alphabet[j]]=temp
	return "".join([perm[c] for c in text])

if __name__ == '__main__':
	f = open(sys.argv[1],'r')
	text = "".join([l.rstrip('\n') for l in f.readlines()])
	text = [c for c in text if c in string.ascii_letters or c == ' ']
	text = "".join(text).upper()
	f.close()
	print scramble(text)
