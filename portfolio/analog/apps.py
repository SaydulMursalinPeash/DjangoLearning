from django.apps import AppConfig


class AnalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analog'

    def ready(self):
        import analog.signals
