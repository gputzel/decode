decode.py
=========
An implementation of the Metropolis Monte Carlo method for decrypting a ciphertext (cryptogram) according to a simple substition. For background, see [this article](http://math.uchicago.edu/~shmuel/Network-course-readings/MCMCRev.pdf) by Persi Diaconis.

See [decode.py in action](https://asciinema.org/a/YWG7r5NAG1QUYy4BpfYqIS83f) using [asciinema](https://asciinema.org/).

[![asciicast](https://asciinema.org/a/YWG7r5NAG1QUYy4BpfYqIS83f.png)](https://asciinema.org/a/YWG7r5NAG1QUYy4BpfYqIS83f)

The program must be "trained"
on a relatively large sample of plaintext (warandpeace.txt is included for this reason).

Usage:
------
    python decode.py [-v] -c cipher.txt -t training.txt -a alphabet.txt -n numSteps -k kmerLength -o output.txt

`-v` sets verbose mode. The program will print out its 'current' guess of the plaintext every 1000 steps

`-a` is the 'target alphabet.' It is the alphabet of the plaintext as well as the training sample.  Note that the training text will be filtered automatically so that only characters belonging to the target alphabet remain. Also it will be made uppercase!

`-k` is the length of the kmers considered by the algorithm (default:2). For k=1, it tries to match the letter frequencies of the training text. For k=2 it tries to match the frequencies of letter pairs.

`-p` is the "temperature" (default: 1.0) of the Metropolis Monte Carlo algorithm. Use a higher temperature if you find the algorithm getting "stuck" in a wrong solution.

`scramble.py`
-------------
Also provided is a tool `scramble.py`. This just makes it easy to generate example cryptograms from input plaintext. Use it as follows:

    python scramble.py plaintext.txt > output.txt

