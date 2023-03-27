#!/Users/U0027598/.env/bin/python  

## usage: calcAnsAtN_MRR.py answer_file grade_file output_file report_type answer_field answer_threshold error_threshold top_n_ranks

## This program will deliver two types of performance reports
## (1) Percentage of queries with an answer in the top n results
## (2) Conventional table of Answer in the top n ranks, where n is set of 5
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
import ast

if len(sys.argv) != 9:
   print ('usage: calcAnsAtN_MRR.py <answer_file> <grade_file> <output_file> <report_flag> <answer_field> <answer_threshold> <error_threshold> <top_n>')
   sys.exit()

answerFile   = open(sys.argv[1],'r',encoding='utf-8',errors='ignore')  # engine output file
gradeFile    = open(sys.argv[2],'r',encoding='utf-8',errors='ignore')  # grade dictionary
f            = open(sys.argv[3],'a')   # output_file
type         = sys.argv[4]             # report_type 
answerField  = int(sys.argv[5])        # field in csv file containing (numeric) grades
ansThreshold = float(sys.argv[6])      # answer threshold
errThreshold = float(sys.argv[7])      # error threshold
n            = int(sys.argv[8])        # top N


qryIdField = 1
rankField = 11
taskField = 4

gQryIdField = 0
gRankField = 1
gradeField = 2

gradeCnt = 0
qryCnt  = 0
qaPairCnt = 0
cumQAPairCnt = 0

isAnsCurrent10 = 0
aCntPerTop10 = 0
isF_Current10 = 0
fCntPerTop10 = 0

mrrAnswers = 0
mrrErrors = 0

ansRank1 = 0
ansRank2 = 0
ansRank3 = 0
ansRank4 = 0
ansRank5 = 0
ansRank6 = 0
ansRank7 = 0
ansRank8 = 0
ansRank9 = 0
ansRank10 = 0

isAnsRank1 = 0
isAnsRank2 = 0
isAnsRank3 = 0
isAnsRank4 = 0
isAnsRank5 = 0
isAnsRank6 = 0
isAnsRank7 = 0
isAnsRank8 = 0
isAnsRank9 = 0
isAnsRank10 = 0

fThreshold = 0.25  # Errors defined as F-F or F-D editor assessments (now unused: converted to a cmd line input: errThreshold)
fRank1 = 0
fRank2 = 0
fRank3 = 0
fRank4 = 0
fRank5 = 0
fRank6 = 0
fRank7 = 0
fRank8 = 0
fRank9 = 0
fRank10 = 0

isfRank1 = 0
isfRank2 = 0
isfRank3 = 0
isfRank4 = 0
isfRank5 = 0
isfRank6 = 0
isfRank7 = 0
isfRank8 = 0
isfRank9 = 0
isfRank10 = 0

c = arr.array('I', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])              # Count of grades for each rank
g = arr.array('I', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])              # Grade counter for each rank
aCnt = arr.array('I', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])        # 'A' counter for each rank
fCnt = arr.array('I', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])        # 'F' counter for each rank
# a = arr.Array('d', [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])  # Average grade per rank

#
# Create Grade Dictionary
# 

print("\nReading in grade dictionary ...")

#for gradeData in gradeFile:
#    gradeCnt += 1
#    grade_dict = (gradeData.split(":")[0]:gradeData.split(":")[1]).rstrip("\n")

#grade_dict = {gradeData.split(":")[0]:gradeData.split(":")[1].rstrip('\n') for gradeData in gradeFile}

gradeData = gradeFile.read().rstrip("\n")
grade_dict = ast.literal_eval(gradeData)  
dict_size = len(grade_dict)

gradeFile.close()

print("Done reading in grade dictionary: " + str(dict_size) + " entries loaded. \n")

#
# Generate Graded Results (Answers) File 
#

for answerData in answerFile:
    qaPairCnt += 1
    cumQAPairCnt += 1
    answerData = answerData.rstrip('\n')
    answerData = answerData.split('\t')
#   taskId    = gradeData[taskField]    
#   aGrade    = float(gradeData[gradeField])
#   aGrade    = 1
    ansString = answerData[answerField] 
    ansGrade  = grade_dict.get(ansString)
    aQryId    = answerData[qryIdField]
    aRank     = answerData[rankField]

    if (ansGrade != None):  # Enter no. grade = -1 for missing grades
        gradeCnt += 1
        f.write(str(aQryId) +"\t" + str(aRank) + "\t" + str(ansGrade) + "\t" + ansString + "\n")
    else:
        f.write(str(aQryId) +"\t" + str(aRank) + "\t" + "-1" + "\t" + ansString + "\n")
#        print(str(aQryId) +"\t" + str(aRank) + "\t" + "-1" + "\t" + ansString + "\n")

#    if (cumQAPairCnt == 2):
#       print(str(ansString))
#       print(ansGrade)

f.close()

#
# Estimate Performance of Current Results using Grade Records
#

qaPairCnt = 0

f = open(sys.argv[3],'r',encoding='utf-8',errors='ignore')   # output_file --> input_file 

for gradeRecord in f: 
    qaPairCnt += 1
    gradeRecord = gradeRecord.strip('\n')
    gradeRecord = gradeRecord.split('\t')
    aGrade = float(gradeRecord[gradeField])
    aRank  = gradeRecord[gRankField]

    if (aGrade >= ansThreshold):
        isAnsCurrent10 = 1
#        f.write(gradeData[gQry<IdField] + "\n")  # Output query id for answer passage
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
            isAnsRank5 = 1
        elif (qaPairCnt == 6 and isAnsRank1 != 1 and isAnsRank2 != 1 and isAnsRank3 != 1 and isAnsRank4 != 1 and isAnsRank5 != 1) :
            aCnt[6] += 1
            isAnsRank6 = 1
        elif (qaPairCnt == 7 and isAnsRank1 != 1 and isAnsRank2 != 1 and isAnsRank3 != 1 and isAnsRank4 != 1 and isAnsRank5 != 1 and isAnsRank6 != 1):
            aCnt[7] += 1
            isAnsRank7 = 1
        elif (qaPairCnt == 8 and isAnsRank1 != 1 and isAnsRank2 != 1 and isAnsRank3 != 1 and isAnsRank4 != 1 and isAnsRank5 != 1 and isAnsRank6 != 1 and isAnsRank7 != 1):
            aCnt[8] += 1
            isAnsRank8 = 1
        elif (qaPairCnt == 9 and isAnsRank1 != 1 and isAnsRank2 != 1 and isAnsRank3 != 1 and isAnsRank4 != 1 and isAnsRank5 != 1 and isAnsRank6 != 1 and isAnsRank7 != 1 and isAnsRank8 != 1):
            aCnt[9] += 1
            isAnsRank9 = 1
        elif (qaPairCnt == 10 and isAnsRank1 != 1 and isAnsRank2 != 1 and isAnsRank3 != 1 and isAnsRank4 != 1 and isAnsRank5 != 1 and isAnsRank6 != 1 and isAnsRank7 != 1 and isAnsRank8 != 1 and isAnsRank9 != 1):
            aCnt[10] += 1
    if (aGrade <= errThreshold):
        isF_Current10 = 1
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
            isfRank5 = 1
        elif (qaPairCnt == 6 and isfRank1 != 1 and isfRank2 != 1 and isfRank3 != 1 and isfRank4 != 1 and isfRank5 != 1):
            fCnt[6] += 1
            isfRank6 = 1
        elif (qaPairCnt == 7 and isfRank1 != 1 and isfRank2 != 1 and isfRank3 != 1 and isfRank4 != 1 and isfRank5 != 1 and isfRank6 != 1):
            fCnt[7] += 1
            isfRank7 = 1
        elif (qaPairCnt == 8 and isfRank1 != 1 and isfRank2 != 1 and isfRank3 != 1 and isfRank4 != 1 and isfRank5 != 1 and isfRank6 != 1 and isfRank7 != 1):
            fCnt[8] +=1
            isfRank8 = 1
        elif (qaPairCnt == 9 and isfRank1 != 1 and isfRank2 != 1 and isfRank3 != 1 and isfRank4 != 1 and isfRank5 != 1 and isfRank6 != 1 and isfRank7 != 1 and isfRank8 != 1):
            fCnt[9] += 1
            isfRank9 = 1
        elif (qaPairCnt == 10 and isfRank1 != 1 and isfRank2 != 1 and isfRank3 != 1 and isfRank4 != 1 and isfRank5 != 1 and isfRank6 != 1 and isfRank7 != 1 and isfRank8 != 1 and isfRank9 != 1):
            fCnt[10] += 1
    if (qaPairCnt == 10):
        qaPairCnt = 0
        qryCnt += 1
        isAnsRank1 = 0
        isAnsRank2 = 0
        isAnsRank3 = 0
        isAnsRank4 = 0
        isAnsRank5 = 0
        isAnsRank6 = 0
        isAnsRank7 = 0
        isAnsRank8 = 0
        isAnsRank9 = 0
        isfRank1 = 0
        isfRank2 = 0
        isfRank3 = 0
        isfRank4 = 0
        isfRank5 = 0
        isfRank6 = 0
        isfRank7 = 0
        isfRank8 = 0
        isfRank9 = 0
        if (isAnsCurrent10 == 1):
            aCntPerTop10 += 1
            isAnsCurrent10 = 0
        if (isF_Current10 == 1):
            fCntPerTop10 += 1
            isF_Current10 = 0

ansRank1 = aCnt[1]
ansRanks1_2 = aCnt[1] + aCnt[2]
ansRanks1_3 = ansRanks1_2 + aCnt[3]
ansRanks1_4 = ansRanks1_3 + aCnt[4]
ansRanks1_5 = ansRanks1_4 + aCnt[5]
ansRanks1_6 = ansRanks1_5 + aCnt[6]
ansRanks1_7 = ansRanks1_6 + aCnt[7]
ansRanks1_8 = ansRanks1_7 + aCnt[8]
ansRanks1_9 = ansRanks1_8 + aCnt[9]
ansRanks1_10 = ansRanks1_9 + aCnt[10]

fRank1 = fCnt[1]
fRanks1_2 = fCnt[1] + fCnt[2]
fRanks1_3 = fRanks1_2 + fCnt[3]
fRanks1_4 = fRanks1_3 + fCnt[4]
fRanks1_5 = fRanks1_4 + fCnt[5]
fRanks1_6 = fRanks1_5 + fCnt[6]
fRanks1_7 = fRanks1_6 + fCnt[7]
fRanks1_8 = fRanks1_7 + fCnt[8]
fRanks1_9 = fRanks1_8 + fCnt[9]
fRanks1_10 = fRanks1_9 + fCnt[10]

mrrAnswers = ((aCnt[1]*1.0) + (aCnt[2]*0.5) + (aCnt[3]*0.333) + (aCnt[4]*0.25) + (aCnt[5]*0.20) + (aCnt[6]*0.167) + (aCnt[7]*0.143) + (aCnt[8]*0.125) + (aCnt[9]*0.111) + (aCnt[10]*0.1))/qryCnt
mrrErrors  = ((fCnt[1]*1.0) + (fCnt[2]*0.5) + (fCnt[3]*0.333) + (fCnt[4]*0.25) + (fCnt[5]*0.20) + (fCnt[6]*0.167) + (fCnt[7]*0.143) + (fCnt[8]*0.125) + (fCnt[9]*0.111) + (fCnt[10]*0.1))/qryCnt

print("gradeCnt = " + str(gradeCnt))
print("cumQAPairCnt = " + str(cumQAPairCnt))
print("Percent of QA Pairs with grades = %0.1f" %(gradeCnt/cumQAPairCnt * 100) + "% \n")

print("\n")
print("Total number of queries: " + str(qryCnt) + "\n")

print("ANSWER SUMMARY (cutoff grade = " + str(ansThreshold) + ")" )
print("--------------")
print("Total number of queries with answer in top *1*: " + str(aCnt[1]) )
print("Percent of queries with answer in top *1*: %0.4f \n" %(aCnt[1]/qryCnt) )

print("Total number of queries with answer in top *3*: " + str(ansRanks1_3) )
print("Percent of queries with answer in top *3*: %0.4f \n" %(ansRanks1_3/qryCnt) )

print("Total number of queries with answer in top *5*: " + str(ansRanks1_5) )
print("Percent of queries with answer in top *5x*: %0.4f \n" %(ansRanks1_5/qryCnt) )

print("Total number of queries with answer in top *10*: " + str(aCntPerTop10) )
print("Percent of queries with answer in top *10*: %0.4f \n" %(aCntPerTop10/qryCnt) )    

print("ERROR SUMMARY (cutoff grade = " + str(errThreshold) + ")" )
print("-------------") 
print("Total number of queries with error in top *1*: " + str(fCnt[1]) )
print("Percent of queries with error in top *1*: %0.4f \n" %(fCnt[1]/qryCnt) )

print("Total number of queries with error in top *3*: " + str(fRanks1_3) )
print("Percent of queries with error in top *3*: %0.4f \n" %(fRanks1_3/qryCnt) )

print("Total number of queries with error in top *5*: " + str(fRanks1_5) )
print("Percent of queries with error in top *5*: %0.4f \n" %(fRanks1_5/qryCnt) )

print("Total number of queries with error in top *10*: " + str(fCntPerTop10) )
print("Percent of queries with error in top *10*: %0.4f \n" %(fCntPerTop10/qryCnt) )


print("ANSWER & ERROR TABLES")
print("---------------------")
print("Answers in ranks 1(" + str(aCnt[1]) + "), 2(" + str(aCnt[2]) + "), 3(" + str(aCnt[3]) + "), 4(" + str(aCnt[4]) + "), 5(" + str(aCnt[5]) + ")" )
#print("Answers in ranks 1(" + str(ansRank1) + "), 2(" + str(ansRanks1_2) + "), 3(" + str(ansRanks1_3) + "), 4(" + str(ansRanks1_4) + "), 5(" + str(ansRanks1_5) + ")" )
print("Ans@1: %0.4f " %(ansRank1/qryCnt) )
print("Ans@2: %0.4f " %(ansRanks1_2/qryCnt) )
print("Ans@3: %0.4f " %(ansRanks1_3/qryCnt) )
print("Ans@4: %0.4f " %(ansRanks1_4/qryCnt) )
print("Ans@5: %0.4f " %(ansRanks1_5/qryCnt) )
print("Ans@6: %0.4f " %(ansRanks1_6/qryCnt) )
print("Ans@7: %0.4f " %(ansRanks1_7/qryCnt) )
print("Ans@8: %0.4f " %(ansRanks1_8/qryCnt) )
print("Ans@9: %0.4f " %(ansRanks1_9/qryCnt) )
print("Ans@10: %0.4f " %(ansRanks1_10/qryCnt) )

print("\n")
print("Errors in ranks 1(" + str(fCnt[1]) + "), 2(" + str(fCnt[2]) + "), 3(" + str(fCnt[3]) + "), 4(" + str(fCnt[4]) + "), 5(" + str(fCnt[5]) + ")" )
print("Err@1: %0.4f " %(fRank1/qryCnt) )
print("Err@2: %0.4f " %(fRanks1_2/qryCnt) )
print("Err@3: %0.4f " %(fRanks1_3/qryCnt) )
print("Err@4: %0.4f " %(fRanks1_4/qryCnt) )
print("Err@5: %0.4f " %(fRanks1_5/qryCnt) )
print("Err@6: %0.4f " %(fRanks1_6/qryCnt) )
print("Err@7: %0.4f " %(fRanks1_7/qryCnt) )
print("Err@8: %0.4f " %(fRanks1_8/qryCnt) )
print("Err@9: %0.4f " %(fRanks1_9/qryCnt) )
print("Err@10: %0.4f " %(fRanks1_10/qryCnt) )
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

