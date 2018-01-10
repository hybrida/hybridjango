import django.dispatch
from django.db.models.signals import pre_save, post_save, post_delete, post_init
from django.core.signals import request_finished
from django.dispatch import receiver
from apps.achievements.models import *
from apps.griffensorden.models import *
from apps.registration.models import *
from .signals import *
from datetime import datetime


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
    if Badge.objects.filter(name="Medlemskaps Medalje").exists():
        badge = Badge.objects.get(name="Medlemskaps Medalje")
        if inst_obj.member == True: #if not awarded already, award the medal
            badge.user.add(inst_obj)
            badge.save()

#function that awards 1,3,5 and 6+ year medals based on the amount of time they have been in Hybrida, not necessarily which year they are in. Also, atm, this function will award these at new years eve, so that you will have the medals for the second semester each year.
@receiver(year_status_change)
def YearBadge(sender, **kwargs):
    inst_obj = kwargs['instance'] #Getting the User
    user = Hybrid.objects.get(username=inst_obj) #getting the users planned graduation date
    grad_year = user.graduation_year
    current_year = int(datetime.now().year) #Getting the current datetime
    medals = [["1års Medalje", 4], ["3års Medalje", 2], ["5års Medalje", 0], ["6+års Medalje", -1]] # list that contains all the year medals we have, consist of elements with the variables name, and what year requirement they need too be achieved
    for medal in medals: #iteration trough every single year Medal, which unfortunatley is hardcoded
        badge = Badge.objects.get(name=medal[0]) #getting each medal for each iteration of the loop
        if grad_year - current_year <= medal[1]:
            badge.user.add(user)
            badge.save()



#===========================================================================================================================#
#functions that provide different utility to the application other than medals
#=============================================================================

#functions that clean up after changed pictures on badges
@receiver(post_init, sender=Badge)
def backup_image_path(sender, instance, **kwargs):
    instance._current_image_file = instance.badge_image

@receiver(post_save, sender=Badge)
def delete_old_image(sender, instance, **kwargs):
    if hasattr(instance, '_current_image_file'):
        if instance._current_image_file != instance.badge_image.path:
            instance._current_image_file.delete(save=False)

#functions that removes pictures after their model has been deleted
def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)

@receiver(models.signals.post_delete, sender=Badge)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    if instance.badge_image:
        _delete_file(instance.badge_image.path)

