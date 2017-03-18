import math
#Log-likelihood
def ll(ciphertext,perm,mat,k):
    s=0.0
    for i in range(len(ciphertext)-(k-1)):
        kmer = tuple([perm[c] for c in ciphertext[i:i+k]])
        s = s + math.log(mat[kmer])
    return s
