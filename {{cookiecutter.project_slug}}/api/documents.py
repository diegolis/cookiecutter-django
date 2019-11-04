{% if cookiecutter.use_elastic %}
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import {{cookiecutter.model_name}}


@registry.register_document
class {{cookiecutter.model_name}}Document(Document):
    class Index:
        name = '{{cookiecutter.model_name}}.Meta.verbose_name_plural'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = {{cookiecutter.model_name}}

        fields = [
        ]
{% endif %}
