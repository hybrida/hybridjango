from django.db import models
from apps.registration.models import Hybrid
from apps.griffensorden.models import Ridder


class Badge(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    badge_image = models.ImageField(upload_to='badges')
    scorepoints = models.PositiveIntegerField()
    user = models.ManyToManyField(Hybrid, blank=True, related_name='hybridbadges')

    def __str__(self):
        return self.name


class BadgeSuggestion(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    award_to = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='badges')
    scorepoints = models.PositiveIntegerField()
    suggested_by = models.ForeignKey(Hybrid, on_delete=models.CASCADE, null=True)


class BadgeRequest(models.Model):
    PENDING = 'P'
    APPROVED = 'A'
    DENIED = 'D'
    CHOICES_STATUS = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (DENIED, 'Denied')
    )
    user = models.ForeignKey(Hybrid, on_delete=models.CASCADE, null=False, blank=False)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, null=False, blank=False)
    comment = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=1,
        choices=CHOICES_STATUS,
        null=False,
        blank=False,
        default=PENDING
    )

    class Meta:
        unique_together = ('badge', 'user',)

    def approve(self):
        self.badge.user.add(self.user)
        self.badge.save()
        self.status = BadgeRequest.APPROVED
        self.save()

    def deny(self):
        self.status = BadgeRequest.DENIED
        self.save()

    def set_pending(self):
        self.status = BadgeRequest.PENDING
        self.save()