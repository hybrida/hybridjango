import django.dispatch
from django.db.models.signals import pre_save, post_save, post_delete, post_init
from django.core.signals import request_finished
from django.dispatch import receiver
from apps.achievements.models import *
from apps.griffensorden.models import *
from apps.registration.models import *
from django.utils import timezone
from .signals import *

#Recievers
@receiver(request_finished)
def my_callback(sender, **kwargs):
    print("Request finished!")

#functions that award specific badges to members based on certain criterias, like membership, if they're ridders and so forth
#===========================================================================================================================#
#function that awards a griffens orden badge to everyone that gets added as a Ridder to the site
@receiver(post_save, sender=Ridder)
def GriffBadge(sender=Ridder, **kwargs):
    inst_obj = kwargs['instance']
    badge = Badge.objects.get(name="Griffens Orden")
    badge.user.add(inst_obj.hybrid)
    badge.save()

#function that awards membership status whenenever the user profiles field for membership returns true
@receiver(post_save, sender=Hybrid)
def MemberBadge(sender=Hybrid, **kwargs):
    inst_obj = kwargs['instance']
    badge = Badge.objects.get(name="Medlemskaps Medalje")
    if inst_obj.member == True: #if not awarded already, award the medal
        badge.user.add(inst_obj)
        badge.save()

#function that awards 1,3,5 and 6+ year medals based on the amount of time they have been in Hybrida, not necessarily which year they are in. Also, atm, this function will award these at new years eve, so that you will have the medals for the second semester each year.
@receiver(year_status_change)
def YearBadge(sender, **kwargs):
    inst_obj = kwargs['instance'] #Getting the User
    grad_year = inst_obj.graduation_year #getting the users planned graduation date
    current_year = timezone.now() #Getting the current datetime
    medals = [["1års Medalje", 4], ["3års Medalje", 2], ["5års medalje", 0], ["6+års Medalje", -1]] # list that contains all the year medals we have, consist of elements with the variables name, and what year requirement they need too be achieved
    for medal in medals: #iteration trough every single year Medal, which unfortunatley is hardcoded
        badge = Badge.objects.get(medal[0]) #getting each medal for each iteration of the loop
        if grad_year - current_year <= medal[1]:
            badge.user.add(inst_obj)
            badge.save()

#===========================================================================================================================#
