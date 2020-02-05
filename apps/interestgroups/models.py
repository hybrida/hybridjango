from django.db import models
from apps.registration.models import *

# Create your models here.
class Season(models.Model):
    SeasonStart = models.DateField
    SeasonEnd = models.DateField

class Match(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    title = models.TextField
    desc = models.TextField
    date = models.DateTimeField
    meetuptime = models.DateTimeField


class Player(models.Model):
    STRIKER = 'S'
    CENTERFORWARD = 'CF'
    LEFTWING = 'LW'
    RIGHTWING = 'RW'
    CENTERATTACKINGMID = 'CAM'
    CENTERDEFENSIVEMID = 'CDM'
    CENTERMID = 'CM'
    LEFTMID = 'LM'
    RIGHTMID = 'RM'
    CENTERBACK = 'CB'
    LEFTBACK = 'LB'
    RIGHTBACK = 'RB'
    KEEPER = 'K'
    POSITON_CHOICES = (
        (STRIKER, 'Striker'),
        (CENTERFORWARD, 'Center Forward'),
        (LEFTWING, 'Left Wing'),
        (RIGHTWING, 'Right Wing'),
        (CENTERATTACKINGMID, 'Center Attacking Midfield'),
        (CENTERDEFENSIVEMID, 'Center Defensive Midfield'),
        (CENTERMID, 'Center Midfield'),
        (LEFTMID, 'Left Midfield'),
        (RIGHTMID, 'Right Midfield'),
        (CENTERBACK, 'Center Back'),
        (LEFTBACK, 'Left Back'),
        (RIGHTBACK, 'Right Back'),
        (KEEPER, 'Keeper')
    )
    
    player = models.ManyToManyField(Hybrid, blank=True)
    captain = models.BooleanField
    goals = models.IntegerField
    assist = models.IntegerField
    position = models.CharField


class Playerlist(models.Model):
    player = models.ManyToManyField(Player)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)


