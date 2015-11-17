import sys
import numpy as np
from sklearn import preprocessing

FAKEDATA = True
NUM_WHITE_CARDS_TOTAL = 538
NUM_LEARNED = 50


# Learning Methods
# 1. Vector Average.
# 2. Probability Weights.
# 3. Category Ranking
METHOD = 2

def main():
	M = np.loadtxt(sys.argv[1],dtype=np.dtype(int),delimiter=',')

	if FAKEDATA:
		whiteWinIDs = np.random.randint(0,high=NUM_WHITE_CARDS_TOTAL,size=NUM_LEARNED)
		chosen = M[whiteWinIDs]

	if METHOD == 1:
		n_chosen = preprocessing.normalize(chosen)
		meanCard = np.mean(n_chosen,axis=0,keepdims=True)
		meanCardNormalized = preprocessing.normalize(meanCard)
		return meanCardNormalized

	if METHOD == 2:
		sumCards = chosen.astype(float).sum(axis=0,keepdims=True)
		weightVector = sumCards/sumCards.sum()
		return weightVector