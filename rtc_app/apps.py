from django.apps import AppConfig


class RtcAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rtc_app'

    def ready(self):
        import rtc_app.signals