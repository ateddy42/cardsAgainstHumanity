import sys
import numpy as np
from sklearn import preprocessing
import learn

FAKE = True
NUM_LEARNED = 50
HAND_SIZE = 7

# Learning Methods
# 1. Vector average.
# 2. Weights, normal.
# 3. Weights, excess over simple random.
# 3. Category Ranking
METHOD = int(sys.argv[1])

M = np.loadtxt('white_cards_features_matrix.csv',dtype=np.dtype(int),delimiter=',')
N = np.loadtxt('black_cards_features_matrix.csv',dtype=np.dtype(int),delimiter=',')
NUM_WHITE_CARDS_TOTAL = M.shape[0]
NUM_BLACK_CARDS_TOTAL = N.shape[0]

preferences = learn.learn(METHOD,FAKE,NUM_WHITE_CARDS_TOTAL,NUM_LEARNED)

if FAKE:
	blackID = np.random.randint(0,high=NUM_BLACK_CARDS_TOTAL)
	whiteIDs = np.random.randint(0,high=NUM_WHITE_CARDS_TOTAL,size=HAND_SIZE)
	blackChosen = N[blackID].astype(float)
	whiteChosen = M[whiteIDs].astype(float)

if METHOD == 1:
	prefarrays = np.repeat(preferences,HAND_SIZE,axis=0)
	diffs = whiteChosen-prefarrays
	norms = np.linalg.norm(diffs,axis=1)
	cardID = np.argmin(norms)

if METHOD == 2:
	prefarrays = np.repeat(preferences,HAND_SIZE,axis=0)
	weightedSum = np.multiply(whiteChosen,prefarrays)
	scores = np.sum(weightedSum,axis=1)
	cardID = np.argmax(scores)

if METHOD == 3:
	prefarrays = np.repeat(preferences,HAND_SIZE,axis=0)
	weightedSum = np.multiply(whiteChosen,prefarrays)
	scores = np.sum(weightedSum,axis=1)
	cardID = np.argmax(scores)

print cardID
