#!/Users/U0027598/anaconda3/bin/python

#!/Users/U0027598/.env/bin/python  

## usage: grabTAMqrys.py

## Strategy: Given a large file of PL Search queries
##    * Grab thosee queries that satisfy the definition of a TAM query:
##        * 5 <= LENGTH <= 30 
##        * contains a question word:
##             * {what, when, where, which, how, why, can, may, does, do, are, is, did, how, are} # excluded: will

import sys
import os
import re

if len(sys.argv) != 3:
   print ('usage: grabTAMqrys.py <qry_file> <output_file>')
   sys.exit()

qryFile   = open(sys.argv[1],'r')
f         = open(sys.argv[2],'a')    # output_file


qrys = [ ]
qryCnt = 0
tamCnt = 0

# questionWordList = ["who ", "what", "when", "where", " how ", "which", "why", " can ", " may ", "must", "could", "should", " do ", "does", " is ", " am ", " are ", " did "] # excluded: will is
questionWordList = ["who ", "what", "when", "where", "how", "which", "why", "can", "may", "must", "could", "should", "do", "does", "is", "am", "are", "did"] # excluded: will is

for qryEntry in qryFile:
    qryEntry = qryEntry.rstrip('\n')
    qryEntry = qryEntry.split(",")
    qry = qryEntry[0]
    qryCnt += 1
    qryLgth = len(qry.split(" "))
#    qry = " " + qry
    qryTokens = qry.split()
#   if qryLgth >= 5 and qryLgth <= 30:
    if qryLgth == 3:
#       if ("(" not in qry) and (")" not in qry):
#          if re.search(r'/[ps1-9]', qry) is None:
##             print(qryTokens[0])
#             for qWord in questionWordList:
##                print(qWord + " | " + qryTokens[0])
#                if qWord == qryTokens[0]:        # was qWord in qry
                   f.write(qry + "\n")
##                   print(qry)
                   tamCnt += 1
#                   break

pctTAMqrys = (tamCnt/qryCnt)*100
print("\n" + str(tamCnt) + " total TAM queries found in file containing " + str(qryCnt) + " queries: %0.2f" %(pctTAMqrys) + "%\n")


#   cmCnt=0
#   cms = [ ]

#   for cm in cmFile:
#      cmCnt+=1
#      cm=cm.rstrip('\n')
#      print(cm)
#      cms.append(cm)
#      if cmCnt==10:
#         break

#   for i, cm in enumerate(cms):
#      for j, cm in enumerate(cms[1:]):
#         span1 = nlp(cms[i])
#         span2 = nlp(cms[j])
#         seq = difflib.SequenceMatcher(None, cms[i], cms[j]).ratio()
#         jaro = jellyfish.jaro_winkler(cms[i], cms[j])
#         if (i > j):
#             f.write(str(qryCnt) + "\t" + qrys[qryCnt - 1] + "\t" + cms[i] + "\t" + cms[j] + "\t" + str(span1.similarity(span2)) + "\n") 
#            f.write(cms[i] + "\t" + cms[j] + "\t" + str(seq) + "\t" + str(jaro) + "\t" + str(span1.similarity(span2)) + "\n")

