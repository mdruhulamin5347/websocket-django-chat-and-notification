from typing import Iterable
from django.db import models
from buyer.models import buyers
# Create your models here.
import uuid

class Cars(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    buyer = models.ForeignKey(buyers, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, blank=True)

    def __str__(self):
       return f"{self.name}-{self.price}-{self.buyer}-{self.code}"
    
    # def save(self, *args, **kwargs):
    #     if self.code == "":
    #         self.code = str(uuid.uuid4()).replace("-","").upper()[:10]
    #     return super().save(*args, **kwargs)