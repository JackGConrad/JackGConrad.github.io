#!/Users/U0027598/.env/bin/python  

## usage: extractAboveThreshold.py results_file extract_file threshold

## This program will extract those top-5 results whose rank 1 result has a score above or equal to the input threshold
##

#
#  results_file  = (tab-sep file) grade file
#  extract_file  = (string) name
#  threshold     = decimal 
# 

import re
import sys
import math

if len(sys.argv) != 4:
   print ('usage: extractAboveThreshold.py <results_file> <extract_file> <threshold>')
   sys.exit()

resultsFile  = open(sys.argv[1],'r',encoding='utf-8',errors='ignore')  # log_file
f            = open(sys.argv[2],'a')   # extract_file
threshold    = float(sys.argv[3])      # threshold 

qaResultCnt = 0
qryCnt = 0
extractQryCnt = 0
grab = 0

gradeField = 8
rankField  = 14
scoreField = 23

for qaResult in resultsFile:
    qaResultCnt += 1
    qaResultRow = qaResult
#    if (qaResultCnt) == 1:
#        f.write(qaResultRow)
#        continue
#   qaResult = qaResult.rstrip('\n')
    qaResult = qaResult.split("\t")
    grade = float(qaResult[gradeField])
    rank  = int(qaResult[rankField])    
    score = float(qaResult[scoreField])

#   print(str(grade) + " | " + str(rank) + " | " + str(score))

    if (rank == 1):
#       print(str(grade) + " | " + str(rank) + " | " + str(score))  
        qryCnt += 1
        if (score >= threshold):
            extractQryCnt += 1
            grab = 1
            f.write(qaResultRow)
        else:
            grab = 0
    else:
        if (grab == 1):
           f.write(qaResultRow)

filteredQryCnt = qryCnt - extractQryCnt

print("\n")
print("For threshold = " + str(threshold) + " :")
print("Total number of queries: " + str(qryCnt) )
print("Total number of QA pairs: " + str(qaResultCnt) )
print("Total number of extracted queries: " + str(extractQryCnt) )
print("Total number of filtered queries: "  + str(filteredQryCnt) + "\n")
