{% if cookiecutter.db == 'django' %}
from rest_framework import serializers
from .models import {{cookiecutter.model_name}}

class {{cookiecutter.model_name}}Serializer(serializers.ModelSerializer):
    class Meta(object):
        model = {{cookiecutter.model_name}}
        fields = "__all__"
{% endif %}
