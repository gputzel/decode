import itertools

def learnMatrix(trainingText,alphabet,k):
    mat={}
    for i in range(len(trainingText)-(k-1)):
        kmer = ''.join(trainingText[i:i+k])
        begin = kmer[:k-1]
        end = kmer[1:]
        if begin in mat:
            if end in mat[begin]:
                mat[begin][end] = mat[begin][end] + 1.0
            else:
                mat[begin][end] = 1.0
        else:
            mat[begin] = {end:1.0}
    for begin in mat.keys():
        s = 0.0
        for end in mat[begin].keys():
            s += mat[begin][end]
        for end in mat[begin].keys():
            mat[begin][end] = mat[begin][end]/s
    return mat

def learnVector(trainingText, alphabet):
    '''Compute the single-character distribution of trainingText.'''
    # Initialize dictionary of (character, probability) pairs.
    v = {}
    for c in alphabet:
        v[c] = 0.1  # Avoid zeros.
        
    # Add up occurrences.
    for c in trainingText:
        v[c] = v[c] + 1
    
    # Normalize distribution.    
    norm = sum(v.values())
    for c in alphabet:
        v[c] = v[c]/norm
        
    return v
        
