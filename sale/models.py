from django.db import models

# Create your models here.

from order.models import Orders

class Sales(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.amount)