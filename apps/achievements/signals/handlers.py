import django.dispatch
from django.db.models.signals import pre_save, post_save, post_delete, post_init
from django.core.signals import request_finished
from django.dispatch import receiver
from apps.achievements.models import *
from apps.griffensorden.models import *
from apps.registration.models import *

#signals
griff_badge = django.dispatch.Signal()



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
    if inst_obj.member == True:
        badge.user.add(inst_obj)
        badge.save()

#function that awards 1,3,5 year medals based on the amount of time they have been in Hybrida, not necessarily which year they are in


#===========================================================================================================================#

#Senders
def Send_GriffBadge():
    griff_badge.send(sender=Ridder)