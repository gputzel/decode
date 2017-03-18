import math
#Log-likelihood: case of general k
def ll(ciphertext,perm,mat,k):
    s=0.0
    for i in range(len(ciphertext)-(k-1)):
        kmer = tuple([perm[c] for c in ciphertext[i:i+k]])
        s = s + math.log(mat[kmer])
    return s

##Log-likelihood - hard-coded version for k=1
def ll_k1(ciphertext,perm,mat):
    s=0.0
    for i in range(len(ciphertext)):
        uple = (perm[ciphertext[i]],)
        s = s + math.log(mat[uple])
    return s

##Log-likelihood - hard-coded version for k=2
def ll_k2(ciphertext,perm,mat):
    s=0.0
    for i in range(len(ciphertext)-1):
        pair = (perm[ciphertext[i]],perm[ciphertext[i+1]])
        s = s + math.log(mat[pair])
    return s

##Log-likelihood - hard-coded version for k=3
def ll_k3(ciphertext,perm,mat):
    s=0.0
    for i in range(len(ciphertext)-2):
        triplet = (perm[ciphertext[i]],perm[ciphertext[i+1]],perm[ciphertext[i+2]])
        s = s + math.log(mat[triplet])
    return s

##Log-likelihood - hard-coded version for k=4
def ll_k4(ciphertext,perm,mat):
    s=0.0
    for i in range(len(ciphertext)-3):
        tuple = (perm[ciphertext[i]],perm[ciphertext[i+1]],perm[ciphertext[i+2]],perm[ciphertext[i+3]])
        s = s + math.log(mat[tuple])
    return s

