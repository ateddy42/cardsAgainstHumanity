# Converts csv file containing cards and feature data to a feature matrix
# Feature matrix M stored as comma separated values in txt file with same name as the cards

import sys
import numpy as np

f = open(sys.argv[1])
lines = f.readlines()
num_cards = len(lines)-1
categories = lines[0].strip().split(',')[2:]
num_categories = len(categories)-1
M = np.zeros((num_cards,num_categories))
for i in range(1,num_cards+1):
	values = lines[i].split(',')[2:]
	for j in range(0,num_categories):
		M[i-1][j] = int(values[j])
np.savetxt(sys.argv[1].split('.')[0]+'_matrix.csv',M,fmt='%i',delimiter=',')