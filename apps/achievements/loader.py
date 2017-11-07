from apps.achievements.models import Prerequisites, Badge
from apps.registration.models import Hybrid
from apps.griffensorden.models import Ridder
from apps.achievements.utils import *
from itertools import compress

#A function that checks all the rquirements trough the utils.py file, and then awards all the achievements that should be awarded.
#It has too cycle trough all the different awards, and check their requirements, and check if any Hybrid have completed these.(Positives: simple, Drawbacks, Datasize, and how to regurarly proc the procedures)
#other solution is to check every achievement for every user, while disregarding every acheivement they have already achieved, upon each log in, to see if they have made any progress.(Positives, les use of data, enables pop up functions, Drawback, people will not see they're progress if the dont log inn)
#TODO


def criteriachecker(PreReq, hybrid, badge):
    method_list = 0
    prereq_list = 0
    fin_list = list(compress(method_list, prereq_list))
    something = False
    for method in method_list:
        #Todo something that executes each method, and tracks the result, have to be able too track more than one return statment, and return true or false
        return

    #Todo an if else statement that takes the result of the methods loop. and either award the right badge, or terminates the process without awarding the badge if the requirements havent been met.
    if something is True:
            #Todo use the True variable to award the Badge to teh right Hybrid
        return

    else:
        #Todo use the false variable to not awrd any badge
        return


def awarder(badge, hybrid):
    #Todo is this right?
    badge.user.add(hybrid)
    return