from .models import buyers
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import json


@receiver(post_save, sender=User)
def buyer_create(sender, instance, created ,**kwargs):
    print("buyers created successfull")
    if created:     
        buyers.objects.create(user=instance)

