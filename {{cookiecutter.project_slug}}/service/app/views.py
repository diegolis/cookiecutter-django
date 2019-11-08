{% if cookiecutter.db == 'django' %}
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .models import {{cookiecutter.model_name}}
from .serializers import {{cookiecutter.model_name}}Serializer


class {{cookiecutter.model_name}}ViewSet(ModelViewSet):
    serializer_class = {{cookiecutter.model_name}}Serializer
    queryset = {{cookiecutter.model_name}}.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
    ]
{% endif %}
