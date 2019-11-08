{% if cookiecutter.db == 'django' %}
from django.db import models


class {{cookiecutter.model_name}}(models.Model):
    pass
{% elif cookiecutter.db == 'elastic' %}
class {{cookiecutter.model_name}}(Document):

    class Index:
        name = '{{cookiecutter.model_name.lower}}'
{% elif cookiecutter.db == 'clickhouse' %}
from infi.clickhouse_orm.database import Database
from infi.clickhouse_orm.models import Model
from infi.clickhouse_orm.fields import *
from infi.clickhouse_orm.engines import MergeTree


class {{cookiecutter.model_name}}(Model):

    engine = MergeTree()
{% endif %}
