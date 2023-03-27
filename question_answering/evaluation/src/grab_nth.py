#!/git/work/Projects/TAM/fastText/venv/bin/python
#
import sys
w = sys.argv[1]   # input text file
x = sys.argv[2]   # output train file
y = sys.argv[3]   # output test file
z = int(sys.argv[4])   # every z'th line (i.e., n'th line) 
print(w)
print(x)
print(y)
print(z)
f_out_train = open(x,'w')
f_out_test = open(y, 'w')
with open(w, 'r') as f:
    for v, line in enumerate(f):
        if v % z == 1:
            f_out_test.write(line)
        else:
            f_out_train.write(line)

