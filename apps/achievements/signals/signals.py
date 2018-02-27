import django.dispatch

#signals for badges
year_status_change = django.dispatch.Signal(providing_args=["User"])