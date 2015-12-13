from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from game.models import *
import random, csv

NUM_CARDS_PER_ROUND = 3

def home(request):
    pwd = "p" in request.GET
    can_judge = request.user.groups.filter(name='Judge')
    return render(request, 'home.html', {"can_judge":can_judge, "pwd":pwd})

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

@login_required
def judge(request):
    can_judge = request.user.groups.filter(name='Judge')
    if not can_judge:
        return HttpResponse("You are not authorized to view this page.")
    if len(BlackCards.objects.all()) == 0 or len(WhiteCards.objects.all()) == 0:
        return HttpResponse("Cards missing from database. <a href='/addCards/'>Add cards.</a>")
    if "v" not in request.GET or not is_number(request.GET["v"]):
        return render(request, "judge.html", {"v":-1})
    AIver = request.GET["v"]
    if ("w" in request.GET and "h" in request.GET): # card picked
        try:
            AIwin = AIPlayed.objects.get(handID = request.GET["h"], AIver = AIver).wID == int(request.GET["w"])
        except AIPlayed.DoesNotExist:
            return HttpResponse("Cannot judge. No cards played for AI Version " + AIver + ".")
        p = Judged(judgeID = request.user.id, handID = request.GET["h"],
                    wID = request.GET["w"], AIver = AIver, AIwin=AIwin)
        p.save()
        return HttpResponseRedirect("/judge/?v=" + request.GET["v"])
    judged = Judged.objects.filter(judgeID = request.user.id).filter(AIver = AIver).values_list('handID', flat=True)
    allHands = Hands.objects.filter(numPlayed = NUM_CARDS_PER_ROUND).exclude(id__in = judged)
    if len(allHands) == 0:
        return HttpResponse("No played hands to choose from.")
    hand = allHands.order_by('?').first()
    black = BlackCards.objects.filter(id=hand.bid)
    playedWhites = Played.objects.filter(handID = hand.id).values_list('wID', flat=True)
    whiteIDs = []
    whiteIDs.extend(playedWhites)
    try:
        AICard = AIPlayed.objects.get(handID = hand.id, AIver = AIver)
        whiteIDs.append(AICard.wID)
    except AIPlayed.DoesNotExist:
        return HttpResponse("No cards played for AI Version " + AIver + ".")
    whites = WhiteCards.objects.filter(id__in = whiteIDs).order_by('?')
    return render(request, "judge.html", {"handID":hand.id, "black":black, "whites":whites, "v":AIver, "remaining":len(allHands)})

@login_required
def play(request):
    if len(WhiteCards.objects.all()) == 0 or len(BlackCards.objects.all()) == 0:
        return HttpResponse("Cards missing from database. <a href='/addCards/'>Add cards.</a>")
    if ("w" in request.GET and "h" in request.GET): # card played
        handID = request.GET["h"]
        hand = Hands.objects.get(id=handID)
        if hand.numPlayed >= NUM_CARDS_PER_ROUND:
            return HttpResponseRedirect("/play/") # already enough responses for this hand
        p = Played(playerID = request.user.id, handID = handID, wID = request.GET["w"])
        p.save()
        hand.numPlayed += 1
        hand.save()
        return HttpResponseRedirect("/play/")
    played = Played.objects.filter(playerID = request.user.id).values_list('handID', flat=True)
    allHands = Hands.objects.exclude(id__in = played).exclude(numPlayed = NUM_CARDS_PER_ROUND)
    if len(allHands) == 0:
        return HttpResponse("No hands to choose from. <a href='/genHands/'>Generate hands.</a>")
    hand = allHands.order_by('-numPlayed').first()
    black = BlackCards.objects.filter(id=hand.bid)
    whiteIDs = HandWhites.objects.filter(handID = hand.id).values_list('wID', flat=True)
    whites = WhiteCards.objects.filter(id__in = whiteIDs).order_by('?')
    return render(request, "play.html", {"handID":hand.id, "black":black, "whites":whites})

@login_required
def AIplay(request):
    if "v" not in request.GET:
        return HttpResponse("No version number given. Add '?v=__' to URL. Version number 0 is random cards.")
    try:
        AIver = int(request.GET["v"])
    except:
        return HttpResponse("Not a valid version number: " + request.GET["v"])
    if len(AIPlayed.objects.filter(AIver = AIver)) > 0:
        return HttpResponse("Cards already played for verison 1")
    allHands = Hands.objects.all()
    if AIver == 0:
        for h in allHands:
            whites = HandWhites.objects.filter(handID = h.id).values_list('wID', flat=True)
            p = AIPlayed(AIver = AIver, handID = h.id, wID = random.choice(whites))
            p.save()
        return HttpResponse("Random Cards played.")
    else:
        return HttpResponse("Non-Random cards not programmed yet.")

@login_required
def leaders(request):
    can_judge = request.user.groups.filter(name='Judge')
    if not can_judge:
        return HttpResponse("You are not authorized to view this page.")
    leaders = Played.objects.raw("""SELECT id, playerID, COUNT( handID ) AS count
                                FROM  `game_played` 
                                GROUP BY playerID
                                ORDER BY count DESC""")
    return render(request, "leaders.html", {"leaders":leaders})

@login_required
def graph(request):
    can_judge = request.user.groups.filter(name='Judge')
    if not can_judge:
        return HttpResponse("You are not authorized to view this page.")
    judges = Judged.objects.values('judgeID').distinct().values_list('judgeID', flat=True)

    graphTitle = ['Judge', 'Version 0', 'Version 1', 'Version 2']
    graphData = []

    allJudgeData = ['All Judges']
    AIver = 0
    try:
        allJudgeData += [len(Judged.objects.filter(AIver = AIver, AIwin = 1)) /\
                float(len(Judged.objects.filter(AIver = AIver)))]
    except:
        allJudgeData += [0]
    AIver = 1
    try:
        allJudgeData += [len(Judged.objects.filter(AIver = AIver, AIwin = 1)) /\
                float(len(Judged.objects.filter(AIver = AIver)))]
    except:
        allJudgeData += [0]
    AIver = 2
    try:
        allJudgeData += [len(Judged.objects.filter(AIver = AIver, AIwin = 1)) /\
                float(len(Judged.objects.filter(AIver = AIver)))]
    except:
        allJudgeData += [0]
    graphData += [allJudgeData]

    for j in judges:
        judgeData = [str(User.objects.get(id=j).username)]
        AIver = 0
        try:
            judgeData += [len(Judged.objects.filter(AIver = AIver, judgeID = j, AIwin = 1)) /\
                    float(len(Judged.objects.filter(AIver = AIver, judgeID = j)))]
        except:
            judgeData += [0]
        AIver = 1
        try:
            judgeData += [len(Judged.objects.filter(AIver = AIver, judgeID = j, AIwin = 1)) /\
                    float(len(Judged.objects.filter(AIver = AIver, judgeID = j)))]
        except:
            judgeData += [0]
        AIver = 2
        try:
            judgeData += [len(Judged.objects.filter(AIver = AIver, judgeID = j, AIwin = 1)) /\
                    float(len(Judged.objects.filter(AIver = AIver, judgeID = j)))]
        except:
            judgeData += [0]
        graphData += [judgeData]
    return render(request, "graph.html", {"graphTitle":graphTitle, "graphData":graphData})


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