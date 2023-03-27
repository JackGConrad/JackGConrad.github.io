#!/Users/U0027598/.env/bin/python  

## usage: calcPrecisionAtN.py results_file output_file report_flag grade_field answer_threshold top_n_ranks

## This program will deliver two types of performance reports
## (1) Percentage of queries with an answer in the top 5 results
## (2) Conventional table of Precision in the top n ranks, where n is set of 5
##     Can take a parameter that changes n to something other than 5
##
#
#  results_file = (string) name
#  output_file  = (string) name
#  report_flag  = 1 (Ans in top-n), 2 (Precision@1 thru Precision@n)
#  grade_file   = (int) Grade column (0-based)
#  answer_threshold = (float) to be considered minimum answer score
#  top_n_ranks  = (int) n (number of top ranks to examine)
#
# Map of grades per each rank
#     Assumes same nos. of ranks processed per query
# Rank:     1  2  3  4  5  
# As:     [ n  n  n  n  n ]
# Cs:     [ m  m  m  m  m ]  
# Ds:     [ s  s  s  s  s ] 
# Fs:     [ t  t  t  t  t ] 


import sys
import math
import numpy as np
import array as arr
import os
import re

if len(sys.argv) != 7:
   print ('usage: calcPrecisionAtN.py <results_file> <output_file> <report_flag> <grade_field> <answer_threshold> <top_n>')
   sys.exit()

gradeFile    = open(sys.argv[1],'r',encoding='utf-8',errors='ignore')
f            = open(sys.argv[2],'a')   # output_file
type         = sys.argv[3]             # report_type 
gradeField   = int(sys.argv[4])        # field in csv file containing (numeric) grades
ansThreshold = float(sys.argv[5])      # top N

taskField = 4
rankField = 8

qryCnt  = 0
qaPairCnt = 0
isAnsRank1 = 0
isAnsCurrent5 = 0
aCntPerTop5 = 0
isF_Current5 = 0
fCntPerTop5 = 0

ansRank1 = 0
ansRank2 = 0
ansRank3 = 0
ansRank4 = 0
ansRank5 = 0

fThreshold = 0.5
fRank1 = 0
fRank2 = 0
fRank3 = 0
fRank4 = 0
fRank5 = 0

isfRank1 = 0
isfRank2 = 0
isfRank3 = 0
isfRank4 = 0
isfRank5 = 0

c = arr.array('I', [0, 0, 0, 0, 0, 0])              # Count of grades for each rank
g = arr.array('I', [0, 0, 0, 0, 0, 0])              # Grade counter for each rank
aCnt = arr.array('I', [0, 0, 0, 0, 0, 0, 0])        # 'A' counter for each rank  
fCnt = arr.array('I', [0, 0, 0, 0, 0, 0, 0])        # 'F' counter for each rank
# a = arr.Array('d', [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])  # Average grade per rank

np.zeros((4,5))

for gradeData in gradeFile:
    qaPairCnt += 1
    gradeData = gradeData.rstrip('\n')
    gradeData = gradeData.split(",")
    taskId    = gradeData[taskField]    
    aGrade    = float(gradeData[gradeField])
    aRank     = gradeData[rankField]
    if (aGrade >= ansThreshold):
        isAnsCurrent5 = 1
        isF_Current5 = 1
        if (qaPairCnt == 1):
            aCnt[1] += 1
            isAnsRank1 = 1
        elif (qaPairCnt == 2 and isAnsRank1 != 1):
            aCnt[2] += 1
            isAnsRank2 = 1
        elif (qaPairCnt == 3 and isAnsRank1 != 1 and isAnsRank2 != 1):
            aCnt[3] += 1
            isAnsRank3 = 1
        elif (qaPairCnt == 4 and isAnsRank1 != 1 and isAnsRank2 != 1 and isAnsRank3 != 1):
            aCnt[4] += 1
            isAnsRank4 = 1
        elif (qaPairCnt == 5 and isAnsRank1 != 1 and isAnsRank2 != 1 and isAnsRank3 != 1 and isAnsRank4 != 1):
            aCnt[5] += 1
    if (aGrade <= fThreshold):
        if (qaPairCnt == 1):
            fCnt[1] += 1
            isfRank1 = 1
        elif (qaPairCnt == 2 and isfRank1 != 1):
            fCnt[2] += 1
            isfRank2 = 1
        elif (qaPairCnt == 3 and isfRank1 != 1 and isfRank2 != 1):
            fCnt[3] += 1
            isfRank3 = 1
        elif (qaPairCnt == 4 and isfRank1 != 1 and isfRank2 != 1 and isfRank3 != 1):
            fCnt[4] += 1
            isAnsRank4 = 1
        elif (qaPairCnt == 5 and isfRank1 != 1 and isfRank2 != 1 and isfRank3 != 1 and isfRank4 != 1):
            fCnt[5] += 1
    if (qaPairCnt == 5):
        qaPairCnt = 0
        qryCnt += 1
        isAnsRank1 = 0
        isAnsRank2 = 0
        isAnsRank3 = 0
        isAnsRank4 = 0
        isfRank1 = 0
        isfRank2 = 0
        isfRank3 = 0
        isfRank4 = 0
        if (isAnsCurrent5 == 1):
            aCntPerTop5 += 1
            isAnsCurrent5 = 0
        elif (isF_Current5 == 1):
            fCntPerTop5 += 1
            isF_Current5 = 0

ansRank1 = aCnt[1]
ansRanks1_2 = aCnt[1] + aCnt[2]
ansRanks1_3 = ansRanks1_2 + aCnt[3]
ansRanks1_4 = ansRanks1_3 + aCnt[4]
ansRanks1_5 = ansRanks1_4 + aCnt[5]

fRank1 = fCnt[1]
fRanks1_2 = fCnt[1] + fCnt[2]
fRanks1_3 = fRanks1_2 + fCnt[3]
fRanks1_4 = fRanks1_3 + fCnt[4]
fRanks1_5 = fRanks1_4 + fCnt[5]

print("\n")
print("Total number of queries: " + str(qryCnt) )
print("Total number of answers in top 5: " + str(aCntPerTop5) )
print("Percent of queries with answer in top 5: %0.6f " %(aCntPerTop5/qryCnt) )    
print("\n")
print("Total number of fails in top 5: " + str(fCntPerTop5) )
print("Percent of queries with fail in top 5: %0.6f " %(fCntPerTop5/qryCnt) )
print("\n")
print("Answers in ranks 1(" + str(aCnt[1]) + "), 2(" + str(aCnt[2]) + "), 3(" + str(aCnt[3]) + "), 4(" + str(aCnt[4]) + "), 5(" + str(aCnt[5]) + ")" )
#print("Answers in ranks 1(" + str(ansRank1) + "), 2(" + str(ansRanks1_2) + "), 3(" + str(ansRanks1_3) + "), 4(" + str(ansRanks1_4) + "), 5(" + str(ansRanks1_5) + ")" )
print("P@1: %0.6f " %(ansRank1/qryCnt) )
print("P@2: %0.6f " %(ansRanks1_2/qryCnt) )
print("P@3: %0.6f " %(ansRanks1_3/qryCnt) )
print("P@4: %0.6f " %(ansRanks1_4/qryCnt) )
print("P@5: %0.6f " %(ansRanks1_5/qryCnt) )
print("\n")
print("Failures in ranks 1(" + str(fCnt[1]) + "), 2(" + str(fCnt[2]) + "), 3(" + str(fCnt[3]) + "), 4(" + str(fCnt[4]) + "), 5(" + str(fCnt[5]) + ")" )
print("F@1: %0.6f " %(fRank1/qryCnt) )
print("F@2: %0.6f " %(fRanks1_2/qryCnt) )
print("F@3: %0.6f " %(fRanks1_3/qryCnt) )
print("F@4: %0.6f " %(fRanks1_4/qryCnt) )
print("F@5: %0.6f " %(fRanks1_5/qryCnt) )

#
#   Result of above grade accumulation
#   (1) Count of answers for each rank
#   (2) Count of answers in top 5  
#   (3) Count of queries seen thus far
#

