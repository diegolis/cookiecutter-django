from django.contrib import admin
from autocompletefilter.admin import AutocompleteFilterMixin
from autocompletefilter.filters import AutocompleteListFilter
from better_admin.mixins import ExportCsvMixin

{% if cookiecutter.db == 'django' %}
from .models import {{cookiecutter.model_name}}
class {{cookiecutter.model_name}}Admin(AutocompleteFilterMixin, admin.ModelAdmin, ExportCsvMixin):
    actions = ['export_as_csv']

admin.site.register({{cookiecutter.model_name}}, {{cookiecutter.model_name}}Admin)
{% endif %}
admin.site.site_header = '{{cookiecutter.project_name}} Admin'
