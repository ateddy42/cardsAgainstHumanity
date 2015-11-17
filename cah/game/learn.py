import sys
import numpy as np
from sklearn import preprocessing

FAKE = True
NUM_LEARNED = 50


# Learning Methods
# 1. Vector average.
# 2. Weights, normal.
# 3. Weights, excess over simple random.
# 3. Category Ranking
METHOD = 2

M = np.loadtxt('white_cards_features_matrix.csv',dtype=np.dtype(int),delimiter=',')
NUM_WHITE_CARDS_TOTAL = M.shape[0]

def learn(method,fake,total,learned):
	if fake:
		whiteWinIDs = np.random.randint(0,high=total,size=learned)
		chosen = M[whiteWinIDs].astype(float)

	if method == 1:
		n_chosen = preprocessing.normalize(chosen)
		meanCard = np.mean(n_chosen,axis=0,keepdims=True)
		meanCardNormalized = preprocessing.normalize(meanCard)
		return meanCardNormalized

	if method == 2:
		weightVector = chosen.sum(axis=0,keepdims=True)
		return weightVector

	if method == 3:
		masterTotals = M.sum(axis=0,keepdims=True)
		masterProbabilities = masterTotals/total
		chosenTotals = chosen.sum(axis=0,keepdims=True)
		chosenProbabilities = chosenTotals/learned
		weightVector = chosenProbabilities-masterProbabilities
		return weightVector

def main():
	print learn(METHOD,FAKE,NUM_WHITE_CARDS_TOTAL,NUM_LEARNED)
