#!/Users/U0027598/.env/bin/python  

## usage: calcTAMQryAvgs.py qry_file output_file threshold

## Strategy: Given a list of 1, 2 or 3 results per query
##    Calculate the average score for the set.
##
## Invites a set of algorithmic rules

import sys
import os
import re

if len(sys.argv) != 5:
   print ('usage: calcTAMQryAvgs.py <qry_file> <accept_file> <reject_file> <threshold>')
   sys.exit()

qryFile    = open(sys.argv[1],'r',encoding='utf-8',errors='ignore')
f          = open(sys.argv[2],'a')   # accept_file
d          = open(sys.argv[3],'a')   # reject_file 
threshold = float(sys.argv[4])       # threshold limit

qryLgth = 0
qryCnt  = 1
qryScoreSum = 0
qryScoreAvg = 0
qryScoreCnt = 0
qryInit = 1
qryFirst = 1
qryPrev = ""

for qryData in qryFile:
    qryData = qryData.rstrip('\n')
    qryData = qryData.split("\t")
    qry      = qryData[0]
    qryScore = qryData[4]  # Chngd from [1] for v2 file
    qryRank  = qryData[5]  # Chngd from [2] for v2 file
    qryLgth = len(qry.split())
    if (qry == qryPrev or qryInit):
       qryScoreSum += float(qryScore) 
       qryScoreCnt += 1
       qryInit = 0
       print(qryRank + ":\t" + qryScore + "\t" + qry)
#       f.write(qryRank + ":\t" + qryScore + "\t" + qry + "\n")
    else:
#       qryScoreSum += float(qryScore)
#       if (qryFirst == 0):
#           qryScoreCnt += 1
       qryScoreAvg = (qryScoreSum/qryScoreCnt)
       print("qry = " + qryPrev + " | qryScoreSum = %0.6f | qryScoreCnt = %0.6f | qryScoreAvg = %0.6f" %(qryScoreSum, qryScoreCnt, qryScoreAvg) )
       if (qryScoreAvg >= threshold):
           f.write(str(qryCnt) + "\t" + qryPrev+ "\t%0.6f\n" %(qryScoreAvg) )
       else:
           d.write(str(qryCnt) + "\t" + qryPrev+ "\t%0.6f\n" %(qryScoreAvg) )
       qryScoreSum = float(qryScore)
       qryScoreCnt = 1
       qryFirst = 0
       print(qryRank + ":\t" + qryScore + "\t" + qry)
#       f.write(qryRank + ":\t" + qryScore + "\t" + qry + "\n")
       qryCnt += 1
    qryPrev = qry

# Final Query Average Score Output
#qryScoreSum += float(qryScore)
#qryScoreCnt += 1
qryScoreAvg = (qryScoreSum/qryScoreCnt)
print("qry = " + qryPrev + " | qryScoreSum = %0.6f | qryScoreCnt = %0.6f | qryScoreAvg = %0.6f" %(qryScoreSum, qryScoreCnt, qryScoreAvg) )
if (qryScoreAvg >= threshold):
   f.write(qryCnt + "\t" + qryPrev + "\t%0.6f\n" %(qryScoreAvg) )
else:
   d.write(str(qryCnt) + "\t" + qryPrev+ "\t%0.6f\n" %(qryScoreAvg) )
# print("qryScoreAvg = %0.6f" %(qryScoreAvg) )

#print("Final TAM Query Count is: " + str(qryCnt))


#    while (qry == qryPrev):                                                                                                                                                                                                     #    if any(word in qry.split() for word in qWords):  # concise                                                                                                                                                                  #       if (5 <= qryLgth and qryLgth <= 30) :                                                                                                                                                                                    #           qryCnt += 1        

# for i, cm in enumerate(cms):
#    for j, cm in enumerate(cms[1:]):
#        span1 = nlp(cms[i])
#        span2 = nlp(cms[j])
#        seq = difflib.SequenceMatcher(None, cms[i], cms[j]).ratio()
#        jaro = jellyfish.jaro_winkler(cms[i], cms[j])
#        if (i > j):
#            f.write(cms[i] + "\t" + cms[j] + "\t" + str(seq) + "\t" + str(jaro) + "\t" + str(span1.similarity(span2)) + "\n")
