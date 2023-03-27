#!/Users/U0027598/anaconda3/bin/python

#!/Users/U0027598/.env/bin/python  

## usage: countTAMqrys.py qry_file threshold

## Strategy: Given a file of queries, determine their length and count those with less than n tokens
##    For each group, perform a pairwise set of comparisons in order to identify 
##    * pairs with the highest overlap
##    * identify the longest sequence (warranting removal)
##    * leave only one of set?
## Invites a set of algorithmic rules

import sys
import os
import re

if len(sys.argv) != 4:
   print ('usage: countTAMqrys.py <qry_file> <output_file> <threshold>')
   sys.exit()


qryFile    = open(sys.argv[1],'r',encoding='utf-8',errors='ignore')
f          = open(sys.argv[2],'a')   # output_file
threshold = float(sys.argv[3])       # threshold limit

qryLgth = 0
qryCnt  = 0

for qry in qryFile:
    qry=qry.rstrip('\n')
    qryLgth = len(qry.split())
    if (qryLgth < threshold):
       qryCnt += 1
       print(qry)
       f.write(qry + "\n")

print("Final TAM Query Count for queries less than " + str(threshold) + " tokens = " + str(qryCnt))


