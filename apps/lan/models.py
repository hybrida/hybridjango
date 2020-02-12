from django.db import models
from apps.registration.models import Hybrid


class Team(models.Model):
    """
    Uncomment when comp is added
    class Meta:
        unique_together=('name', 'comp')
    """
    users = models.ManyToManyField(Hybrid, blank=False)

    def default_name(self):
        return self.users.first().full_name

    name = models.CharField(
        max_length=255,
        default=default_name
    )


class Bracket(models.Model):
    # Add foreignkey to comp
    pass


class Match(models.Model):
    teams = models.ManyToManyField(Team)
    next_match = models.ForeignKey('Match', related_name='prev_match', on_delete=models.SET_NULL)
    bracket = models.ForeignKey(Bracket, related_name='matches')


class Scoreboard(models.Model):
    pass


class Entry(models.Model):
    user = models.ForeignKey(Hybrid, null=False, blank=False)
    value = models.DoubleField(null=False, blank=False)
    scoreboard = models.ForeignKey(Scoreboard, related_name='entries', blank=False)
