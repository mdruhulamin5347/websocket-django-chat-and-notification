from django.db import models
from buyer.models import buyers
# Create your models here.
from cars.models import Cars

class Orders(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    car = models.ManyToManyField(Cars)
    total = models.IntegerField(null=True, blank=True)
    total_price = models.IntegerField(null=True,blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)
