from apps.achievements.models import Prerequisites, Badge
from apps.registration.models import Hybrid
from apps.griffensorden.models import Ridder

#A function that checks all the rquirements trough the utils.py file, and then awards all the achievements that should be awarded.
#It has too cycle trough all the different awards, and check their requirements, and check if any Hybrid have completed these.(Positives: simple, Drawbacks, Datasize, and how to regurarly proc the procedures)
#other solution is to check every achievement for every user, while disregarding every acheivement they have already achieved, upon each log in, to see if they have made any progress.(Positives, les use of data, enables pop up functions, Drawback, people will not see they're progress if the dont log inn)
#TODO