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

#function that awards a griffens orden badge to everyone that gets added as a Ridder to the site
@receiver(post_save, sender=Ridder)
def GriffBadge(sender=Ridder, **kwargs):
    inst_obj = kwargs['instance']
    badge= Badge.objects.get(name="Griffens Orden")
    badge.user.add(inst_obj.hybrid)
    badge.save()


#Senders
def Send_GriffBadge():
    griff_badge.send(sender=Ridder)