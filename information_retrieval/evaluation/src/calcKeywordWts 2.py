#!/Users/U0027598/anaconda3/bin/python

## usage: python calcKeywordWts.py file keyword

## TO DO: replace keyword with keyword file
##        replace count with array or hash table recording the counts

import sys

if len(sys.argv) != 4:
   print ('usage: calcKeywordWts.py <keyword_file> <qry_file> <output_file>')
   sys.exit()

keywordFile = open(sys.argv[1],'r')
qryFile = open(sys.argv[2],'r')
f       = open(sys.argv[3],'a')
count = 0
lineno = 0

for key in keywordFile:
   key[:-2]
   print(key)
   for qry in qryFile:
      qry[:-1]
      print(qry)
      if key in qry:
         count += 1
      value = (key,count)
      print(str(value))
   value = (key,count)
#   print(value)
   f.write(str(value))
   count = 0

#   lineno += 1                                                                                                                                                                                                        #   if lineno%1000 == 1:                                                                                                                                                                                               #      print(line)   

#   print('Total',key,'is',count)
