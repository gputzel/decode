import math
#Log-likelihood
def ll(ciphertext,perm,mat):
	s=0.0
	c1 = ciphertext[0]
	for c2 in ciphertext[1:]:
		#print math.log(mat[(perm[c1],perm[c2])])
		s = s + math.log(mat[(perm[c1],perm[c2])])
		c1=c2
	return s