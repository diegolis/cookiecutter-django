from django.db import models

{% if cookiecutter.model_name != "" %}
class {{cookiecutter.model_name}}(models.Model):
    pass
{% endif %}
