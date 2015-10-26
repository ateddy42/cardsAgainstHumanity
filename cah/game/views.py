from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from game.models import *
import random, csv

NUM_CARDS_PER_ROUND = 3

def home(request):
    return render(request, 'home.html', {})

@login_required
def judge(request):
    if len(BlackCards.objects.all()) == 0 or len(WhiteCards.objects.all()) == 0:
        return HttpResponse("Cards missing from database. <a href='/addCards/'>Add cards.</a>")
    if ("w" in request.GET and "h" in request.GET): # card picked
        p = Judged(judgeID = request.user.id, handID = request.GET["h"], wID = request.GET["w"])
        p.save()
        return HttpResponseRedirect("/judge/")
    judged = Judged.objects.filter(judgeID = request.user.id).values_list('handID', flat=True)
    allHands = Hands.objects.filter(numPlayed = NUM_CARDS_PER_ROUND).exclude(id__in = judged)
    if len(allHands) == 0:
        return HttpResponse("No played hands to choose from.")
    hand = allHands.order_by('?').first()
    black = BlackCards.objects.filter(id=hand.bid)
    whiteIDs = Played.objects.filter(handID = hand.id).values_list('wID', flat=True)
    whites = WhiteCards.objects.filter(id__in = whiteIDs)
    return render(request, "judge.html", {"handID":hand.id, "black":black, "whites":whites})

@login_required
def play(request):
    if len(WhiteCards.objects.all()) == 0 or len(BlackCards.objects.all()) == 0:
        return HttpResponse("Cards missing from database. <a href='/addCards/'>Add cards.</a>")
    if ("w" in request.GET and "h" in request.GET): # card played
        handID = request.GET["h"]
        hand = Hands.objects.get(id=handID)
        if hand.numPlayed >= NUM_CARDS_PER_ROUND:
            return HttpResponse("Hand already has enough user responses.")
        p = Played(playerID = request.user.id, handID = handID, wID = request.GET["w"])
        p.save()
        hand.numPlayed += 1
        hand.save()
        return HttpResponseRedirect("/play/")
    played = Played.objects.filter(playerID = request.user.id).values_list('handID', flat=True)
    allHands = Hands.objects.exclude(id__in = played)
    hand = None
    hand2 = allHands.filter(numPlayed = 2)
    if len(hand2) > 0:
        hand = hand2.order_by('?').first()
    else:
        hand1 = allHands.filter(numPlayed = 1)
        if len(hand1) > 0:
            hand = hand1.order_by('?').first()
        else:
            hand0 = allHands.filter(numPlayed = 0)
            if len(hand0) > 0:
                hand = hand0.order_by('?').first()
    if hand is None:
        return HttpResponse("No hands to choose from. <a href='/genHands/'>Generate hands.</a>")
    black = BlackCards.objects.filter(id=hand.bid)
    whiteIDs = HandWhites.objects.filter(handID = hand.id).values_list('wID', flat=True)
    whites = WhiteCards.objects.filter(id__in = whiteIDs).order_by('?')
    return render(request, "play.html", {"handID":hand.id, "black":black, "whites":whites})

@login_required
def addCards(request):
    if len(BlackCards.objects.all()) > 0 or len(WhiteCards.objects.all()) > 0:
        return HttpResponse("Cards already in database.")
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    with open(BASE_DIR + '/game/black_cards.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            _, created = BlackCards.objects.get_or_create(text=row[1])
    with open(BASE_DIR + '/game/white_cards.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            _, created = WhiteCards.objects.get_or_create(text=row[1])
    return HttpResponse("Success")

@login_required
def genHands(request):
    if len(Hands.objects.all()) > 0:
        return HttpResponse("Hands already generated.")
    if len(BlackCards.objects.all()) == 0 or len(WhiteCards.objects.all()) == 0:
        return HttpResponse("Cards missing from database. <a href='/addCards/'>Add cards.</a>")
    numBlacks = len(BlackCards.objects.all())
    numWhites = len(WhiteCards.objects.all())
    random.seed()
    for i in range(500):
        bid = random.randint(1, numBlacks)
        h = Hands(bid = bid)
        h.save()
        for j in range(7):
            wID = random.randint(1, numWhites)
            c = HandWhites(handID = h.id, wID = wID)
            c.save()
    return HttpResponse("Success")