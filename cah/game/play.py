import sys, os
import numpy as np
from sklearn import preprocessing
from models import Judged, Hands, HandWhites, AIPlayed

FAKE = False
NUM_LEARNED = 50
#HAND_SIZE = 7

# Learning Methods
# 1. Vector average.
# 2. Weights, normal.
# 3. Weights, excess over simple random.
# 3. Category Ranking
METHOD = 1

def learn(method, M, chosen):
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
        masterProbabilities = masterTotals/float(len(M))
        chosenTotals = chosen.sum(axis=0,keepdims=True)
        chosenProbabilities = chosenTotals/float(len(chosen))
        weightVector = chosenProbabilities-masterProbabilities
        return weightVector

def playUser(request, userID, AIversion, method):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    M = np.loadtxt(BASE_DIR + '/game/white_cards_features_matrix.csv',dtype=np.dtype(int),delimiter=',')
    N = np.loadtxt(BASE_DIR + '/game/black_cards_features_matrix.csv',dtype=np.dtype(int),delimiter=',')
    NUM_WHITE_CARDS_TOTAL = M.shape[0]
    NUM_BLACK_CARDS_TOTAL = N.shape[0]

    # preferences = learn.learn(METHOD,FAKE,NUM_WHITE_CARDS_TOTAL,NUM_LEARNED)

    # LEARNING
    if FAKE:
        whiteWinIDs = np.random.randint(0,high=total,size=learned)
        chosen = M[whiteWinIDs].astype(float)

    playedWhites = Judged.objects.filter(judgeID = userID).values_list('wID', flat=True)
    if len(playedWhites) == 0:
        return False
    whiteWinIDs = []
    whiteWinIDs.extend(playedWhites)
    whiteWinIDs = [x - 2 for x in whiteWinIDs]
    #whiteWinIDs = np.array(whiteWinIDs)
    chosen = M[whiteWinIDs].astype(float)

    preferences = learn(method, M, chosen)



    for h in Hands.objects.all():
        blackID = h.bid - 2
        whites = HandWhites.objects.filter(handID = h.id).values_list('wID', flat=True)
        whiteIDs = []
        whiteIDs.extend(whites)
        whiteIDs = [x - 2 for x in whiteIDs]
        whiteIDs = np.array(whiteIDs)
        blackChosen = N[blackID].astype(float)
        whiteChosen = M[whiteIDs].astype(float)
        HAND_SIZE = len(whiteChosen)

        # PLAY
        if FAKE:
            blackID = np.random.randint(0,high=NUM_BLACK_CARDS_TOTAL)
            whiteIDs = np.random.randint(0,high=NUM_WHITE_CARDS_TOTAL,size=HAND_SIZE)
            blackChosen = N[blackID].astype(float)
            whiteChosen = M[whiteIDs].astype(float)

        if method == 1:
            prefarrays = np.repeat(preferences,HAND_SIZE,axis=0)
            diffs = whiteChosen-prefarrays
            norms = np.linalg.norm(diffs,axis=1)
            cardID = np.argmin(norms)

        if method == 2:
            prefarrays = np.repeat(preferences,HAND_SIZE,axis=0)
            weightedSum = np.multiply(whiteChosen,prefarrays)
            scores = np.sum(weightedSum,axis=1)
            cardID = np.argmax(scores)

        if method == 3:
            prefarrays = np.repeat(preferences,HAND_SIZE,axis=0)
            weightedSum = np.multiply(whiteChosen,prefarrays)
            scores = np.sum(weightedSum,axis=1)
            cardID = np.argmax(scores)

        # return cardID
        p = AIPlayed(AIver = AIversion, handID = h.id, wID = cardID+2, userID = userID)
        p.save()
    return True