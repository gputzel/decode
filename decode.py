import learn
import likelihood
import sys
import random
import math
from optparse import OptionParser	#Deprecated since Python 2.7 but...

def usage():
    """Print information on how to use decode.py."""
    print "Usage: python decode.py ..."

def decode(ciphertext,targetAlphabet,numSteps,verbose=False):
    return "plaintext"
	
def parse_options():
    """Parse the command line options."""
    parser = OptionParser()
    parser.add_option("-c", "--cipher", dest="ciphertextFilename")
    parser.add_option("-a", "--alphabet", dest="alphabetFilename")
    parser.add_option("-o", "--output", dest="outputFilename")
    parser.add_option("-t", "--training", dest="trainingFilename")
    parser.add_option("-n","--numsteps",dest="numSteps")
    parser.add_option("-k","--kmerLength",dest="k", default='2')
    parser.add_option("-v", "--verbose", action="store_true",dest="verbose", default=False)
    parser.add_option("-p", "--temperature", dest="temperature",default="1.0")
    options, args = parser.parse_args()
    if not options.outputFilename:
        print "Please specify an output file for plain text with option -o"
        sys.exit()
    if not options.ciphertextFilename:
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
        training = "".join(lines).upper() #Make it all uppercase
        training = [c for c in training if c in alphabet] #Only include symbols included in target alphabet
        f.close()
    except IOError:
        print "Error opening training text file " + options.trainingFilename
        sys.exit()

    # Read in ciphertext.    
    try:
        f = open(options.ciphertextFilename)
        ciphertext = "".join([l.rstrip('\n') for l in f.readlines()])
        f.close()
    except IOError:
        print "Error opening ciphertext file " + options.ciphertextFilename
        sys.exit()
    return alphabet, training, ciphertext
    
def init_cipherAlphabet(alphabet, training, ciphertext):
    """Initialize the cipher alphabet and generate the initial guess permutation."""
    # Make sure target alphabet has at least as many symbols as ciphertext.
    cipherAlphabet = list(set(ciphertext))
    if len(cipherAlphabet) > len(alphabet):
        print "Error: ciphertext contains more distinct symbols than target alphabet"
        sys.exit()

    # Special case: If ciphertext alphabet is a subset of target alphabet
    # Then give them the same order
    if set(cipherAlphabet) < set(alphabet):
        cipherAlphabet = alphabet
	    
    # Sort initial guess according to letter frequencies.
    cipherFrequencies = learn.learnVector(ciphertext, cipherAlphabet)
    trainingFrequencies = learn.learnVector(training, alphabet)

    cipherAlphabet = sorted(cipherFrequencies, key=cipherFrequencies.get, reverse=True)
    alphabet = sorted(trainingFrequencies, key=trainingFrequencies.get,reverse=True)
	    
    # Represent two permutations using dictionaries
    # perm is the "current" permutation
    perm={}
    for a,b in zip(cipherAlphabet, alphabet):
        perm[a] = b
        
    return cipherAlphabet, perm
    
def metropolis(ciphertext, cipherAlphabet, perm, transitionMatrix, numSteps,verbose=False,k=2,temperature=1.0):
    perm2 = perm.copy()     # "trial" permutation in Metropolis.
   
    #Choose the appropriate ll function
    #For speed, these have been hard-coded for k=1,2,3
    llfunc = lambda ciphertext, perm, mat: likelihood.ll(ciphertext,perm,mat,k=k)
    if k==1:
        llfunc = likelihood.ll_k1
    if k==2:
        llfunc = likelihood.ll_k2
    if k==3:
        llfunc = likelihood.ll_k3
    if k==4:
        llfunc = likelihood.ll_k4

    # Instead of the likelihood, we work with the log-likelihood
    # This makes it easier to deal with very small likelihoods
    # Initial log-likelihood of the message:
    logl = llfunc(ciphertext,perm,transitionMatrix)
    
    beta = 1.0/temperature
    for t in range(1, numSteps+1):
        # Trial move that permutes symbols with index i and j in the target alphabet
        i = cipherAlphabet[random.randint(0,len(cipherAlphabet)-1)]
        j = cipherAlphabet[random.randint(0,len(cipherAlphabet)-1)]
        # Find log-likelihood of the message with trial move.
        perm2[i]=perm[j]
        perm2[j]=perm[i]
        lltrial=llfunc(ciphertext,perm2,transitionMatrix)
        if lltrial > logl:
            # If the trial permutation produces a higher likelihood, accept it
            logl = lltrial
            perm[i]=perm2[i]
            perm[j]=perm2[j]
        else:
            #If the trial likelihood is lower, still give it a chance of being accepted
            if random.random() < math.exp(beta*(lltrial - logl)):
                # Accept trial move.
                logl=lltrial
                perm[i]=perm2[i]
                perm[j]=perm2[j]
            else:
                # Reject trial move.
                perm2[i]=perm[i]
                perm2[j]=perm[j]
        if t % 1000 == 0:
            if verbose:
                print "Step ", t
                print "".join([perm[c] for c in ciphertext])
    return perm
    
def main():
    options, args = parse_options()
    
    alphabet, training, ciphertext = read_texts(options)
	    
    # Learn the transition matrices from the training text.
    if options.verbose:
        print "Learning transition matrix from training text..."
    transitionMatrix = learn.learnMatrix(training, alphabet, int(options.k))
        
    # Initialize correspondence between cipher symbols and alphabet.
    cipherAlphabet, perm = init_cipherAlphabet(alphabet, training, ciphertext)
    
    if options.verbose:
        print "Initial guess"
        print "".join([perm[c] for c in ciphertext]) # Initial guess.
    
    # Metropolis algorithm.
    perm = metropolis(ciphertext, cipherAlphabet, perm, transitionMatrix,
                      int(options.numSteps), options.verbose, int(options.k),float(options.temperature))
    	
    # Write the output.
    try:
        f = open(options.outputFilename,'w')
        f.write("".join([perm[c] for c in ciphertext]))
        f.close()
    except IOError:
        print "Error: Could not open output file " + options.outputFilename
        sys.exit()
	    		
if __name__ == "__main__":
    main()


