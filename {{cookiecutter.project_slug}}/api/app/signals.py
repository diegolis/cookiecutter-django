from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import {{cookiecutter.model_name}}


"""
@receiver(post_save, sender={{cookiecutter.model_name}})
def process(sender, instance, **kwargs):
    pass
"""
