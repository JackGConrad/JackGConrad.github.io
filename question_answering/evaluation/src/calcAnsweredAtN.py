#!/Users/U0027598/.env/bin/python  

## usage: calcAnsweredAtN.py results_file output_file report_flag grade_field answer_threshold top_n_ranks

## This program will deliver two types of performance reports
## (1) Percentage of queries with an answer in the top n ranks
## (2) Conventional table of Answered in the top n ranks, where n is typically set at 5
##     Can take a parameter that changes n to something other than 5
##
##     The program will do the same for errors in the top n ranks. 
#
#  results_file = (string) name
#  output_file  = (string) name
#  report_flag  = 1 (Ans in top-n), 2 (Precision@1 thru Precision@n)
#  grade_file   = (int) Grade column (0-based)
#  answer_threshold = (float) to be considered minimum answer score
#  error_threshold  = (float) to be considered the maximum error score
#  top_n_ranks  = (int) n (number of top ranks to examine)
#


import sys
import math
import numpy as np
import array as arr
import os
import re

if len(sys.argv) != 8:
   print ('usage: calcPrecisionAtN.py <results_file> <output_file> <report_flag> <grade_field> <answer_threshold> <error_threshold> <top_n>')
   sys.exit()

gradeFile    = open(sys.argv[1],'r',encoding='utf-8',errors='ignore')
f            = open(sys.argv[2],'a')   # output_file
type         = sys.argv[3]             # report_type 
gradeField   = int(sys.argv[4])        # field in csv file containing (numeric) grades
ansThreshold = float(sys.argv[5])      # answer threshold
errThreshold = float(sys.argv[6])      # error threshold
n            = int(sys.argv[7])        # top N

# N.B. number_grade column is input on command line.  The following three fields are entered below.

rankField = 12
qryIdField = 2
taskField = 5

qryCnt  = 0
qaPairCnt = 0
isAnsCurrent5 = 0
aCntPerTop5 = 0
isF_Current5 = 0
fCntPerTop5 = 0

mrrAnswers = 0
mrrErrors = 0

ansRank1 = 0
ansRank2 = 0
ansRank3 = 0
ansRank4 = 0
ansRank5 = 0

isAnsRank1 = 0
isAnsRank2 = 0
isAnsRank3 = 0
isAnsRank4 = 0
isAnsRank5 = 0

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


for gradeData in gradeFile:
    qaPairCnt += 1
    gradeData = gradeData.rstrip('\n')
    gradeData = gradeData.split("\t")
    taskId    = gradeData[taskField]    
    aGrade    = float(gradeData[gradeField])
    aRank     = gradeData[rankField]
    if (aGrade >= ansThreshold):
        isAnsCurrent5 = 1
        # f.write(gradeData[qryIdField] + "\n")  # Output query id for answer passage
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
    if (aGrade <= errThreshold):
        isF_Current5 = 1
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
            isfRank4 = 1
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
        else:
            f.write(gradeData[qryIdField] + "\n")  
        if (isF_Current5 == 1):
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

mrrAnswers = ((aCnt[1]*1.0) + (aCnt[2]*0.5) + (aCnt[3]*0.333) + (aCnt[4]*0.25) + (aCnt[5]*0.20))/qryCnt
mrrErrors   = ((fCnt[1]*1.0) + (fCnt[2]*0.5) + (fCnt[3]*0.333) + (fCnt[4]*0.25) + (fCnt[5]*0.20))/qryCnt

print("\n")
print("Total number of queries: " + str(qryCnt) + "\n")

print("ANSWER SUMMARY (cutoff grade = " + str(ansThreshold) + ")" )
print("--------------")
print("Total number of queries with answer in top *1*: " + str(aCnt[1]) )
print("Percent of queries with answer in top *1*: %0.4f \n" %(aCnt[1]/qryCnt) )

print("Total number of queries with answer in top *3*: " + str(ansRanks1_3) )
print("Percent of queries with answer in top *3*: %0.4f \n" %(ansRanks1_3/qryCnt) )

print("Total number of queries with answer in top *5*: " + str(aCntPerTop5) )
print("Percent of queries with answer in top *5*: %0.4f \n" %(aCntPerTop5/qryCnt) )    

print("ERROR SUMMARY (cutoff grade = " + str(errThreshold) + ")" )
print("-------------") 
print("Total number of queries with error in top *1*: " + str(fCnt[1]) )
print("Percent of queries with error in top *1*: %0.4f \n" %(fCnt[1]/qryCnt) )

print("Total number of queries with error in top *3*: " + str(fRanks1_3) )
print("Percent of queries with error in top *3*: %0.4f \n" %(fRanks1_3/qryCnt) )

print("Total number of queries with error in top *5*: " + str(fCntPerTop5) )
print("Percent of queries with error in top *5*: %0.4f \n" %(fCntPerTop5/qryCnt) )


print("ANSWER & ERROR TABLES")
print("---------------------")
print("Answers in ranks 1(" + str(aCnt[1]) + "), 2(" + str(aCnt[2]) + "), 3(" + str(aCnt[3]) + "), 4(" + str(aCnt[4]) + "), 5(" + str(aCnt[5]) + ")" )
print("Ans@1: %0.4f " %(ansRank1/qryCnt) )
print("Ans@2: %0.4f " %(ansRanks1_2/qryCnt) )
print("Ans@3: %0.4f " %(ansRanks1_3/qryCnt) )
print("Ans@4: %0.4f " %(ansRanks1_4/qryCnt) )
print("Ans@5: %0.4f " %(ansRanks1_5/qryCnt) )
print("\n")
print("Errors in ranks 1(" + str(fCnt[1]) + "), 2(" + str(fCnt[2]) + "), 3(" + str(fCnt[3]) + "), 4(" + str(fCnt[4]) + "), 5(" + str(fCnt[5]) + ")" )
print("Err@1: %0.4f " %(fRank1/qryCnt) )
print("Err@2: %0.4f " %(fRanks1_2/qryCnt) )
print("Err@3: %0.4f " %(fRanks1_3/qryCnt) )
print("Err@4: %0.4f " %(fRanks1_4/qryCnt) )
print("Err@5: %0.4f " %(fRanks1_5/qryCnt) )
print("\n")
print("MEAN RECIPROCAL RANK SUMMARY")
print("----------------------------")
print("Mean Reciprocal Rank for *Answers* in top " + str(n) + " ranks: %0.4f" %(mrrAnswers) + " (min-max values: [0, 1.0] )")
print("Mean Reciprocal Rank for *Errors* in top " + str(n) + " ranks: %0.4f"  %(mrrErrors) + " (min-max values: [0, 1.0] )")
print("\n")
#
#   Result of above grade accumulation
#   (1) Count of answers for each rank
#   (2) Count of answers in top 5  
#   (3) Count of queries seen thus far
#

