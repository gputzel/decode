decode.py
=========
An implementation of the Metropolis Monte Carlo method for decrypting a ciphertext (cryptogram) according to a simple substition. For background, see [this article](http://math.uchicago.edu/~shmuel/Network-course-readings/MCMCRev.pdf) by Persi Diaconis.

The program must be "trained"
on a relatively large sample of plaintext (warandpeace.txt is included for this reason).

Usage:
------
    python decode.py [-v] -c cipher.txt -t training.txt -a alphabet.txt -n numSteps -o output.txt

`-v` sets verbose mode. The program will print out its 'current' guess of the plaintext every 1000 steps

`-a` is the 'target alphabet.' It is the alphabet of the plaintext as well as the training sample.  Note that the training text will be filtered automatically so that only characters belonging to the target alphabet remain. Also it will be made uppercase!

`scramble.py`
-------------
Also provided is a tool `scramble.py`. This just makes it easy to generate example cryptograms from input plaintext. Use it as follows:

    python scramble.py plaintext.txt > output.txt

