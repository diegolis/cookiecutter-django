from rest_framework.viewsets import ModelViewSet
from .models import {{cookiecutter.model_name}}
from django.db.models import Q
from users.models import InfoxelUser
from .serializers import {{cookiecutter.model_name}}Serializer
from django_filters.rest_framework import DjangoFilterBackend


class {{cookiecutter.model_name}}ViewSet(ModelViewSet):
    serializer_class = {{cookiecutter.model_name}}Serializer
    queryset = {{cookiecutter.model_name}}.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
    ]
