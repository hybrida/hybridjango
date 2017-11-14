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

@receiver(post_save, sender=Ridder)
def GriffBadge(sender=Ridder, **kwargs):
    inst_obj = kwargs['instance']
    badge= Badge.objects.get(name="Griffens Orden")
    print(inst_obj.hybrid) #kaller flere objekter!!!!!
    badge.user.add(inst_obj.hybrid)
    badge.save()


#Senders
def Send_GriffBadge():
    griff_badge.send(sender=Ridder)