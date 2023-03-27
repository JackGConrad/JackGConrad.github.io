#!/Users/U0027598/anaconda3/bin/python

#!/Users/U0027598/.env/bin/python  

## usage: findSimCMs.py cm_file output_file threshold

## Strategy: Given a list of 10 or more CMs
##    For each group, perform a pairwise set of comparisons in order to identify 
##    * pairs with the highest overlap
##    * identify the longest sequence (warranting removal)
##    * leave only one of set?
## Invites a set of algorithmic rules

import sys
import os
import re
import difflib
import jellyfish
import spacy
import unicodedata
#import sense2vec
#from sense2vec import Sense2VecComponent

if len(sys.argv) != 4:
   print ('usage: findSimCMs.py <cm_file> <output_file> <threshold>')
   sys.exit()

nlp = spacy.load('en_vectors_web_lg')
n_vectors = 105000 # no. of vectors to keep
#removed_words = nlp.vocab.prune_vectors(n_vectors)

# assert len(nlp.vocab.vectors) <= n_vectors # unique vectors have been pruned                                                                                                                                           
# assert nlp.vocab.vectors.n_keys > n_vectors #

############################################################
#s2v = sense2vec.load('/path/to/reddit_vectors-1.1.0')

#s2v = Sense2VecComponent('/path/to/reddit_vectors-1.1.0')                                                                                                                                                             
#nlp.add_pipe(s2v)
############################################################                                       

cmFile    = open(sys.argv[1],'r',encoding="latin-1")
f         = open(sys.argv[2],'a')    # output_file
threshold = float(sys.argv[3])       # threshold limit
cms = [ ]                            # declare CM array
pairCount = 0

for cm in cmFile:
    cm=cm.rstrip('\n')
    print(cm)
    cms.append(cm)

for i, cm in enumerate(cms):
    for j, cm in enumerate(cms[1:]):
        span1 = nlp(cms[i])
        span2 = nlp(cms[j])
        seq = difflib.SequenceMatcher(None, cms[i], cms[j]).ratio()
        jaro = jellyfish.jaro_winkler(cms[i], cms[j])
        if (i > j):
            f.write(cms[i] + "\t" + cms[j] + "\t" + str(seq) + "\t" + str(jaro) + "\t" + str(span1.similarity(span2)) + "\n")

#   lineno += 1
#   if lineno%1000
#      print(line)   
