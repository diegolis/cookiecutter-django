{% if cookiecutter.db == 'django' %}
from rest_framework.routers import SimpleRouter
from .views import {{cookiecutter.model_name}}ViewSet
from django.conf.urls import url

router = SimpleRouter()

router.register(r'{{cookiecutter.model_name.lower()}}s', {{cookiecutter.model_name}}ViewSet)

urlpatterns = router.urls
{% endif %}
