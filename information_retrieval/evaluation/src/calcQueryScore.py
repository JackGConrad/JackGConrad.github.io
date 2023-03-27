#!/Users/U0027598/anaconda3/bin/python

## usage: python calcQueryScore.py qry_file keyword_file output_file

##
## Strategy: Process query file, query-by-query,
##    For each query, check to see if there is a match with a keyword in the keyword file
##    * Do not consider entries < 4 characters in length
##    * Require an exact match between the query terms and the term in the keyword string
##    * Do not consider multi-term expressions
##    * Remove extraneous trailing query characters like '?'  
##    * Sum the freqeuncy counts for each matched term
##    * Write out to a file the query and its final cumulative 'score'
##    * Tab-separate output fields to permit sorting queries by final score
##

import sys
import os
import re
import subprocess

if len(sys.argv) != 5:
   print ('usage: calcQueryScore.py <query_file> <keyword_file> <output_file> <weighting_type>')
   sys.exit()

queryFile   = open(sys.argv[1],'r')
#keywordFile = open(sys.argv[2],'r')   # moved below
f           = open(sys.argv[3],'a')    # output_file
weight_type = sys.argv[4]              # weight_type = 'ALL' uses all entries (n-grams)
count = 0
score = 0
lineno = 0

for query in queryFile:
    query=query.rstrip('\n')
    query=query.rstrip('?')
#   print(query)
    keywordFile = open(sys.argv[2],'r',encoding='mac_roman')
    for keystring in keywordFile:
#        print(lineno)
#        lineno += 1 
        keywordStr=keystring.split('\t')[0]
        keywordScore=keystring.split('\t')[1].rstrip('\n')
        keywords=keywordStr.split(' ')
        if len(keywords)==1 and len(keywordStr) > 3 and keywordStr in query:
              exactQueryWords=query.split(' ')
              if keywordStr in exactQueryWords:
                  count += 1
                  score += int(keywordScore)
#                 f.write(str(query) + " | " + str(keywordStr) + " | " + str(keywordScore) + " | " + str(score) + "\n")
                  print(str(query) + " | " + str(keywordStr) + " | " + str(keywordScore) + "\n")
        elif  len(keywords)==2 and len(keywords[1]) > 1 and keywordStr in query:
#              str_concat = ' ' + keywords[0] + ' ' 
#              print( '*' + str_concat + '*' + '\n')
              if len(keywords[0]) < 3 and (' ' + keywords[0] + ' ') in query:
                  count += 1
                  score += int(keywordScore)
#                 f.write(str(query) + " | " + str(keywordStr) + " | " + str(keywordScore) + " | " + str(score) + "\n")
                  print(str(query) + " | " + str(keywordStr) + " | " + str(keywordScore) + "\n")
              elif len(keywords[0]) > 2:
                  count += 1
                  score += int(keywordScore)
#                 f.write(str(query) + " | " + str(keywordStr) + " | " + str(keywordScore) + " | " + str(score) + "\n")
                  print(str(query) + " | " + str(keywordStr) + " | " + str(keywordScore) + "\n")
        elif  weight_type == "ALL" and len(keywords) > 2 and keywordStr in query:
              count += 1
              score += int(keywordScore)
#             f.write(str(query) + " | " + str(keywordStr) + " | " + str(keywordScore) + " | " + str(score) + "\n")
              print(str(query) + " | " + str(keywordStr) + " | " + str(keywordScore) + "\n")
    f.write(str(query) + "\t" + str(score) + "\n")
    score=0
    del(keywordFile)

print("calcQueryScore processing completed with " + str(count) + " matches.") 

#   lineno += 1
#   if lineno%1000
#      print(line)   

#   print('Total',key,'is',count)
