from optparse import OptionParser	#Deprecated since Python 2.7 but...
import sys
import learn
import likelihood
import os
import random
import math

def parse_options():
    """Parse the command line options."""
    parser = OptionParser()
    parser.add_option("-c", "--cipher", dest="ciphertextFilenames", action="append")
    parser.add_option("-a", "--alphabet", dest="alphabetFilename")
    parser.add_option("-o", "--output", dest="outputFilename")
    parser.add_option("-t", "--training", dest="trainingFilename")
    parser.add_option("-n","--numsteps",dest="numSteps")
    parser.add_option("-k","--kmerLength",dest="k", default='2')
    parser.add_option("-v", "--verbose", action="store_true",dest="verbose", default=False)
    parser.add_option("-p", "--temperature", dest="temperature",default="1.0")
    parser.add_option("-g", "--guessKey",dest="initialGuess", default=None)

    options, args = parser.parse_args()
    if not options.outputFilename:
        print "Please specify an output file for plain text with option -o"
        sys.exit()
    if not options.ciphertextFilenames:
        print "Please specify ciphertext file with option -c"
        sys.exit()
    if not options.trainingFilename:
        print "Please specify training text filename with option -t"
        sys.exit()
    if not options.alphabetFilename:
        if options.verbose:
            print "Reading target alphabet from alphabet.txt"
        alphabetFilename = "alphabet.txt"
    else:
        alphabetFilename = options.alphabetFilename
    if not options.numSteps:
        print "Please specify a number of Monte Carlo steps with option -n"
        sys.exit()
    else:
        steps = int(options.numSteps)
    return options, args

def read_texts(options):
    """Read in target alphabet, training text, and ciphertext."""
    # Read in target alphabet.
    try:
        f = open(options.alphabetFilename,'r')
        alphabet = [c for c in f.readline().rstrip('\n')]
        f.close()
    except IOError:
        print "Error opening alphabet file " + alphabetFilename
        sys.exit()
        
    # Read in training text.  
    try:
        if options.verbose:
            print "Reading training text from " + options.trainingFilename + "..."
        f = open(options.trainingFilename)
        lines = f.readlines()
        training = "".join(lines).upper()
        training = [c for c in training if c in alphabet] #Only include symbols included in target alphabet
        f.close()
    except IOError:
        print "Error opening training text file " + options.trainingFilename
        sys.exit()

    if options.initialGuess:
        with open(options.initialGuess,'rb') as fg:
            initialGuess = bytearray(fg.read())
    else:
        initialGuess = None

    # Read in ciphertexts.    
    ciphertexts=[]
    for cFilename in options.ciphertextFilenames:
        try:
            fc = open(cFilename,"rb")
            ciphertexts.append(bytearray(fc.read().rstrip('\n')))
        except IOError:
            print "Error opening ciphertext file " + cFilename
    return alphabet, training, ciphertexts,initialGuess

def printable(i):
    if i < 32:
        return False
    if i > 126:
        return False
    return True

def checkPlaintexts(message,plaintexts,ciphertexts,key,alphabet,length):
    for ptext,ctext in zip(plaintexts,ciphertexts):
        for i in range(length):
            #if ptext[i] != (ctext[i] ^ key[i]):
            #    print message, "Violated XOR condition"
            #    sys.exit()
            if not(ptext[i] in alphabet):
                print message, "Violated alphabet condition"
                print "In plaintext: ", ptext
                sys.exit()


def metropolis(ciphertexts,alphabet,tmat,numSteps,verbose,k,temperature,initialGuess):
    beta = 1.0/temperature

    alphabetASCII = set([ord(c) for c in alphabet])

    #First, truncate everything to the shortest ciphertext
    #Note that the len(ctext) - 1 gets rid of the line end at the end of the plaintexts
    #Might not be what we want, in the end.
    cipherlength = min([len(ctext)-1 for ctext in ciphertexts])
    ciphertexts = [ctext[:cipherlength] for ctext in ciphertexts]

    #print "Last characters of ciphertexts: "
    #for ctext in ciphertexts:
    #    print ctext[-1]

    #Initialize the key so that each of its characters is at least printable
    key = bytearray(cipherlength)
    #for i in range(cipherlength):
    #    for char in range(256):
    #        if all([printable(char ^ ctext[i]) for ctext in ciphertexts]):
    #            #print "All printable ", i, char
    #            key[i] = char
    #            break

    #Keep track of the "workable" positions - those for which there
    #is at least one possible key value that makes all of the corresponding
    #plaintexts (at that position) members of the target alphabet
    validPositions = []
    possibleKeyValues = {}

    #For each position of the valid positions, we'll keep track
    #of how often each possible value is taken
    keyValueCounts = {}

    #Try to find an initial guess such that as many as possible of the ciphertext
    #letters are in the target alphabet
    for i in range(cipherlength):
        keyvalues = []
        for char in range(256):
            hits = [(char ^ ctext[i]) in alphabetASCII for ctext in ciphertexts]  
            if all(hits):
                #print "All in alphabet ", i, char
                keyvalues.append(char)
                key[i] = char
                #break
        if len(keyvalues) > 0:
            validPositions.append(i)
            possibleKeyValues[i] = keyvalues
            keyValueCounts[i] = {c:0 for c in keyvalues}

    if initialGuess:
        key = initialGuess

    plaintexts = [bytearray(cipherlength) for _ in ciphertexts]
    
    for ptext,ctext in zip(plaintexts,ciphertexts):
        for pos in range(cipherlength):
            ptext[pos] = key[pos] ^ ctext[pos]

    #for ptext in plaintexts:
    #    print 'Plain text ', str(ptext)
    #    print 'Last character ', ptext[-1]
    ll = sum([likelihood.plaintextLL(str(ptext),tmat,k) for ptext in plaintexts])
    print "Likelihood: ", ll
    print '******'
    #checkPlaintexts("A",plaintexts,ciphertexts,key,alphabetASCII,cipherlength)

    for t in range(1,numSteps+1):
        #Update keyValueCounts
        #for i in range(len(key)):
        #    keyValueCounts[i][key[i]] = keyValueCounts[i][key[i]] + 1
        for pos in keyValueCounts.keys():
            keyValueCounts[pos][key[pos]] = keyValueCounts[pos][key[pos]] + 1
        #ll = sum([likelihood.plaintextLL(str(ptext),tmat,k) for ptext in plaintexts])
        #Trial move that changes a random letter
        #Only choose among the "workable" positions
        randomIndex = random.randint(0,len(validPositions)-1)
        pos = validPositions[randomIndex]
        newvalue = possibleKeyValues[pos][random.randint(0,len(possibleKeyValues[pos])-1)]
        #newCharPrintable = False
        #pos = random.randint(0,cipherlength-1)
        oldvalue = key[pos]

        #We don't need to evaluate the likelihood over the entire texts
        start = max(0,pos-k)
        stop = min(cipherlength,pos+k+1)
        
        ll = sum([likelihood.plaintextLL(str(ptext[start:stop]),tmat,k) for ptext in plaintexts])
        
        ###END NEW SECTION
        #checkPlaintexts("A2",plaintexts,ciphertexts,key,alphabetASCII,cipherlength)        
        #We're not even going to try any moves that don't preserve printability
        #while not newCharPrintable:
        #    newvalue = random.randint(0,255)
        #    #newCharPrintable = all([printable(ctext[pos] ^ newvalue) for ctext in ciphertexts])
        #    ##Make sure 
        #    newCharPrintable = all([(ctext[pos] ^ newvalue) in alphabetASCII for ctext in ciphertexts])
        #checkPlaintexts("B",plaintexts,ciphertexts,key,alphabetASCII,cipherlength)        
        key[pos] = newvalue
        for ptext,ctext in zip(plaintexts,ciphertexts):
            ptext[pos] = key[pos] ^ ctext[pos]
        #checkPlaintexts("C",plaintexts,ciphertexts,key,alphabetASCII,cipherlength)
        lltrial = sum([likelihood.plaintextLL(str(ptext[start:stop]),tmat,k) for ptext in plaintexts])
        #If lltrial > ll, then do nothing (keep the change)
        if lltrial < ll:
            if random.random() > math.exp(beta*(lltrial - ll)):
                #Reject the move
                key[pos] = oldvalue
      
        #checkPlaintexts("D",plaintexts,ciphertexts,key,alphabetASCII,cipherlength)

        if t % 1000 == 0:
            if verbose:
                print "Step ", t
        for ptext,ctext in zip(plaintexts,ciphertexts):
            for pos in range(cipherlength):
                ptext[pos] = key[pos] ^ ctext[pos]
            if t % 1000 == 0:
                if verbose:
                    print ptext
        if t % 1000 ==  0:
            if verbose:
                #print "Log-likelihood: ", ll
                print ''.join(['-'*cipherlength])
    
    #Find "most likely" key
    mostLikelyKey = bytearray(len(key))
    for i in range(len(key)):
        record = 0
        mostLikelyChar = -1
        for c in keyValueCounts[i].keys():
            if keyValueCounts[i][c] > record:
                record = keyValueCounts[i][c]
                mostLikelyChar = c
        mostLikelyKey[i] = mostLikelyChar
   
    for ptext,ctext in zip(plaintexts,ciphertexts):
            ptext[pos] = mostLikelyKey[pos] ^ ctext[pos]

    return mostLikelyKey,plaintexts

def main():
    options, args = parse_options()
    alphabet, training, ciphertexts,initialGuess = read_texts(options)
    # Learn the transition matrices from the training text.
    if options.verbose:
        print "Learning transition matrix from training text..."
    transitionMatrix = learn.learnMatrix(training, alphabet, int(options.k))

    key, plaintexts = metropolis(ciphertexts,alphabet,transitionMatrix,int(options.numSteps),options.verbose,
            int(options.k),float(options.temperature),initialGuess)

    for ptext in plaintexts:
        print ptext

    with open(options.outputFilename,'wb') as fout:
        fout.write(key)

if __name__ == "__main__":
    main()
