from django.apps import AppConfig


class ServiceConfig(AppConfig):
    name = 'app'

    def ready(self):
        import .signals
