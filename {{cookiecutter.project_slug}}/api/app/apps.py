from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'app'

    def ready(self):
        import .signals
