from django.db import models

from apps.registration.models import Hybrid


class GitlabToken(models.Model):
    hybrid = models.OneToOneField(Hybrid, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}, primary_key=True, related_name='gitlab_token')
    token = models.CharField(max_length=50, blank=False, verbose_name='Private Token')

    def __str__(self):
        return self.hybrid.get_username()
