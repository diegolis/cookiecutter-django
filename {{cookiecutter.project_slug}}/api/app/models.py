from django.db import models

{% if cookiecutter.function_name %}
class {{cookiecutter.model_name}}(models.Model):
    pass
{% endif %}
