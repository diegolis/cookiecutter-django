from django.contrib import admin
from .models import {{cookiecutter.model_name}}
from autocompletefilter.admin import AutocompleteFilterMixin
from autocompletefilter.filters import AutocompleteListFilter
from better_admin.mixins import ExportCsvMixin

admin.site.site_header = '{{cookiecutter.project_name}} Admin'

{% if cookiecutter.function_name %}
class {{cookiecutter.model_name}}Admin(AutocompleteFilterMixin, admin.ModelAdmin, ExportCsvMixin):
    actions = ['export_as_csv']

admin.site.register({{cookiecutter.model_name}}, {{cookiecutter.model_name}}Admin)
{% endif %}
