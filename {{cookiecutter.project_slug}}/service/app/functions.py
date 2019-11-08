{% cookiecutter.db == 'django' %}
from functions.base import *
from .models import {{cookiecutter.model_name}}
from .serializers import {{cookiecutter.model_name}}Serializer


class {{cookiecutter.model_name}}Mixin(BaseFunction):
    model = {{cookiecutter.model_name}}
    model_name = '{{cookiecutter.model_name.lower}}'
    serializer = {{cookiecutter.model_name}}Serializer


class {{cookiecutter.model_name}}CreateFunction({{cookiecutter.model_name}}Mixin, CreateFunction):
    pass


class {{cookiecutter.model_name}}UpdateFunction({{cookiecutter.model_name}}Mixin, UpdateFunction):
    pass


class {{cookiecutter.model_name}}DeleteFunction({{cookiecutter.model_name}}Mixin, DeleteFunction):
    pass
{% endif %}
