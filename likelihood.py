import math
#Log-likelihood of a ciphertext: case of general k
def ciphertextLL(ciphertext,perm,mat,k):
    s=0.0
    for i in range(len(ciphertext)-(k-1)):
        kmer = ''.join([perm[c] for c in ciphertext[i:i+k]])
        begin = kmer[:k-1]
        end = kmer[1:]
        if (begin in mat) and (end in mat[begin]):
            s = s + math.log(mat[begin][end])
        else: #Assign it some low likelihood
            s = s - 10.0
    return s

#Log-likelihood of a proposed plaintext
def plaintextLL(plaintext,mat,k):
    s=0.0
    for i in range(len(plaintext)-(k-1)):
        kmer = plaintext[i:i+k]
        begin = kmer[:k-1]
        end = kmer[1:]
        if (begin in mat) and (end in mat[begin]):
            s = s + math.log(mat[begin][end])
        else: #Assign it some low likelihood
            s = s - 10.0
    return s

#Log-likelihood of a proposed plaintext
def plaintextLL2(plaintext,mat,k):
    s=0.0
    for i in range(len(plaintext)-(k-1)):
        kmer = plaintext[i:i+k]
        begin = kmer[:k-1]
        end = kmer[1:]
        print begin,end
        if (begin in mat) and (end in mat[begin]):
            print "delta = ", math.log(mat[begin][end])
            s = s + math.log(mat[begin][end])
        else: #Assign it some low likelihood
            print "minus 10"
            s = s - 10.0
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

