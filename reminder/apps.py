from django.apps import AppConfig


class ReminderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reminder'

    def ready(self):
        import reminder.signals

default_app_config = 'reminder.apps.MyAppConfig'
