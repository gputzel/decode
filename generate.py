import learn
import sys
import random
from optparse import OptionParser	#Deprecated since Python 2.7 but...

def parse_options():
    """Parse the command line options."""
    parser = OptionParser()
    parser.add_option("-a", "--alphabet", dest="alphabetFilename")
    parser.add_option("-t", "--training", dest="trainingFilename")
    parser.add_option("-n","--numchars",dest="numChars")
    parser.add_option("-k","--kmerLength",dest="k", default='2')
    options, args = parser.parse_args()
    if not options.trainingFilename:
        print "Please specify training text filename with option -t"
        sys.exit()
    if not options.alphabetFilename:
        if options.verbose:
            print "Reading target alphabet from alphabet.txt"
        alphabetFilename = "alphabet.txt"
    else:
        alphabetFilename = options.alphabetFilename
    if not options.numChars:
        print "Please specify a number of output characters with option -n"
        sys.exit()
    else:
        steps = int(options.numChars)
    return options, args

def read_texts(options):
    """Read in target alphabet, training text"""
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
        f = open(options.trainingFilename)
        lines = f.readlines()
        training = "".join(lines).upper() #Make it all uppercase
        training = [c for c in training if c in alphabet] #Only include symbols included in target alphabet
        f.close()
    except IOError:
        print "Error opening training text file " + options.trainingFilename
        sys.exit()
    return alphabet, training

def generateString(transitionMatrix,alphabet,numChars,k):
    wpbegin="WELL PRINCE SO GENOA AND LUCCA"
    wpbeginnospace="WELLPRINCESOGENOAANDLUCCA"
    
    if '_' in alphabet:
        state=wpbegin[:k-1]
    else:
        state=wpbeginnospace[:k-1]
    state = tuple([c for c in state])
    charList = [c for c in state]
    for _ in range(numChars):
        r = random.random()
        s = 0.0
        for c in alphabet:
            s = s + transitionMatrix[state + (c,)]
            if s > r:
                break
        charList.append(c)
        state = state[1:] + (c,)
    return ''.join(charList)

def main():
    options, args = parse_options()
    numChars = int(options.numChars)
    alphabet, training = read_texts(options)
    transitionMatrix = learn.learnMatrix(training, alphabet, int(options.k))    
    print generateString(transitionMatrix,alphabet,numChars,int(options.k))

if __name__ == "__main__":
    main()
