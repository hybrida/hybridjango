from apps.achievements.models import Badge, Prerequisites
from apps.griffensorden.models import Ridder
from apps.registration.models import Hybrid



#write your utility for the different medals here, the definitions should contain a method for checking the requirements, and if it is correct, it should return True, else it should not return anything
#=======================================================================================================================================================================================================#
#utility too check if the requirement for Ridder has been met
class Criterias:
    def griffmedal(Hyb_pk):
            isKnight = Ridder.objects.filter(name__exact=Hybrid.get_full_name)
            if isKnight is not None:
                return True

    #utility too check for the Vago medal, this might be a personal award only for the moment, which then might not need a utility
    def vagomedal(Hyb_pk):
            #Todo
            return None

    #utilty for awarding a year medal, has to be programmed so it can take a variety of years
    def yearmedal(Hyb_pk):
            #Todo
            return None

    #utility for awarding a commitee medal, this might be a personal award only, as there is no tracking of membership in commitees at the site yet
    def commiteemedal(Hyb_pk):
            #Todo
            return None

    #utility for awarding membership medals, Using the member value of Hybrid
    def membershipmedal(Hyb_pk):
            #Todo
            return None

    #utility for awarding a jubileums medal, should probably check for participation in events with a jubileums tag, and then award it based on that. SHOULD BE REUSEABLE!!!
    def jubmedal(Hyb_pk):
            #Todo
            return None

    #utility for awarding members of the council their hard earned award. Should check with the council page on staticpages, and compare that with the individual Hybrid.
    def councilmedal(Hyb_pk):
            #Todo
            return None

    #Utility for awarding medals to winners of a quiz, will be award only until/if the quiz application ever gets to be used
    def quizmedal(Hyb_pk):
           #Todo
            return None