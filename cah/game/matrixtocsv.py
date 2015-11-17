# Converts feature matrix file to original csv containing cards
# made this because i was stupid and rewrote the original file when trying to create a matrix file
# so had to recreate the original file from the matrix

# sys.argv[1] is the template without any feature numbers (e.g. white_cards.csv)
# sys.argv[2] is the matrix file
# new file with addition _matrix.csv will be created

import sys
import numpy as np

filename = sys.argv[1]
M = np.loadtxt(sys.argv[2],dtype=np.dtype(int),delimiter=',')
f = open(filename)
g = open(filename.split('.')[0]+'NEW.csv','w')
lines = f.readlines()
g.write(lines[0])
for i in range(1,len(lines)):
	line = lines[i]
	linelist = line.split(',')
	for j in range(0,M.shape[1]):
		linelist[j+2] = str(M[i-1][j])
	linestring = ','.join(linelist)
	g.write(linestring)