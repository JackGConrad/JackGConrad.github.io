#!/Users/U0027598/anaconda3/bin/python

#!/Users/U0027598/.env/bin/python  

## usage: grabTAMqrys.py cm_file output_file 

## Strategy: Given a list of 10 or more CMs
##    For each group, perform a pairwise set of comparisons in order to identify 
##    * pairs with the highest overlap
##    * identify the longest sequence (warranting removal)
##    * leave only one of set?
## Invites a set of algorithmic rules

import sys
import os
import re

if len(sys.argv) != 3:
   print ('usage: grabTAMqrys.py <cm_file> <output_file')
   sys.exit()


qryFile    = open(sys.argv[1],'r',encoding='utf-8',errors='ignore')
f          = open(sys.argv[2],'a')    # output_file
#threshold = float(sys.argv[3])       # threshold limit

qWords  = ['who','what','when','where','how','which','do','does','is','am','are','can','could','should','must','may']   # declare 16 term qWord array
qryLgth = 0
qryCnt  = 0

for evalData in qryFile:
    qry = evalData.split("\t")[0]
    qry=qry.rstrip('\n')
    qryLgth = len(qry.split())
    if any(word in qry.split() for word in qWords):  # concise
       if (5 <= qryLgth and qryLgth <= 30) :
           qryCnt += 1
           print(qry)
           f.write(qry + "\n")

print("Final TAM Query Count is: " + str(qryCnt))



# for i, cm in enumerate(cms):
#    for j, cm in enumerate(cms[1:]):
#        span1 = nlp(cms[i])
#        span2 = nlp(cms[j])
#        seq = difflib.SequenceMatcher(None, cms[i], cms[j]).ratio()
#        jaro = jellyfish.jaro_winkler(cms[i], cms[j])
#        if (i > j):
#            f.write(cms[i] + "\t" + cms[j] + "\t" + str(seq) + "\t" + str(jaro) + "\t" + str(span1.similarity(span2)) + "\n")
