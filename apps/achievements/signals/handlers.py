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

@receiver(pre_save, sender=Ridder)
def GriffBadge(sender=Ridder, **kwargs):
    badge= Badge.objects.get(name="Griffens Orden")
    badge.user.add(sender.hybrid)
    badge.save()


#Senders
def Send_GriffBadge():
    griff_badge.send(sender=Ridder)