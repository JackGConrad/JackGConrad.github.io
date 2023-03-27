#!/Users/U0027598/anaconda3/bin/python

#!/Users/U0027598/.env/bin/python  

## usage: findSimCMs.py qry_file cm_file output_file threshold

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

if len(sys.argv) != 5:
   print ('usage: findSimCMs.py <qry_file> <cm_file> <output_file> <threshold>')
   sys.exit()

nlp = spacy.load('en_vectors_web_lg')
n_vectors = 105000 # no. of vectors to keep

qryFile   = open(sys.argv[1],'r')
cmFile    = open(sys.argv[2],'r')
f         = open(sys.argv[3],'a')    # output_file
threshold = float(sys.argv[4])       # threshold limit
qrys = [ ]
cms  = [ ]                            # declare CM array
qryCnt = 0 # 2
cmCnt = 0

for qry in qryFile:
   qry=qry.rstrip('\n')
   qrys.append(qry)

while qryCnt < 1000: 
   qryCnt+=1
   cmCnt=0
   cms = [ ]
   for cm in cmFile:
      cmCnt+=1
      cm=cm.rstrip('\n')
      print(cm)
      cms.append(cm)
      if cmCnt==10:
         break

   for i, cm in enumerate(cms):
      for j, cm in enumerate(cms[1:]):
         span1 = nlp(cms[i])
         span2 = nlp(cms[j])
#         seq = difflib.SequenceMatcher(None, cms[i], cms[j]).ratio()
#         jaro = jellyfish.jaro_winkler(cms[i], cms[j])
         if (i > j):
             f.write(str(qryCnt) + "\t" + qrys[qryCnt - 1] + "\t" + cms[i] + "\t" + cms[j] + "\t" + str(span1.similarity(span2)) + "\n") 
#            f.write(cms[i] + "\t" + cms[j] + "\t" + str(seq) + "\t" + str(jaro) + "\t" + str(span1.similarity(span2)) + "\n")

