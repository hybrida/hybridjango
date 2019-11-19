from apps.events.models import Event, EventType

for event in Event.objects.all():
    event.type = EventType.objects.first()
    event.save()
