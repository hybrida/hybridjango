from django.apps import AppConfig

class AchievementsConfig(AppConfig):
    name = 'apps.achievements'
    verbose_name = 'Achievements'

    def ready(self):
        from apps.achievements.signals import handlers, signals