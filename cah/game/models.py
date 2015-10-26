from django.db import models

class BlackCards(models.Model):
    id = models.AutoField(max_length="4", primary_key=True)
    text = models.TextField(max_length="200", default='')

class WhiteCards(models.Model):
    id = models.AutoField(max_length="4", primary_key=True)
    text = models.TextField(max_length="200", default='')

class Hands(models.Model):
    id = models.AutoField(max_length="10", primary_key=True)
    bid = models.IntegerField(default=0)
    numPlayed = models.IntegerField(default=0)

class HandWhites(models.Model):
    handID = models.IntegerField(default=0)
    wID = models.IntegerField(default=0)

class Played(models.Model):
    id = models.AutoField(max_length="10", primary_key=True)
    playerID = models.IntegerField(default=0)
    handID = models.IntegerField(default=0)
    wID = models.IntegerField(default=0)

class Judged(models.Model):
    id = models.AutoField(max_length="10", primary_key=True)
    judgeID = models.IntegerField(default=0)
    handID = models.IntegerField(default=0)
    wID = models.IntegerField(default=0)