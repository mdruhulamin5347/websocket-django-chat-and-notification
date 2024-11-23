from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Cars
import uuid
from buyer.models import buyers

@receiver(pre_save, sender=Cars)
def code_pre_save(sender, instance,**kwargs):
    if instance.code == "":
        instance.code = str(uuid.uuid4()).replace("-","").upper()[:10]

    obj = buyers.objects.get(user = instance.buyer.user)
    obj.available = True
    obj.save()
