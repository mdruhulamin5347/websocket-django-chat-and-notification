from cars.models import Cars
from .models import Orders
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from sale.models import Sales


@receiver(m2m_changed, sender=Orders.car.through)
def order_total_and_totalprice(sender, instance, action,**kwargs):
        total = 0
        total_price = 0
        for i in instance.car.all():
            print(i.name)
            total += 1
            total_price += i.price

        instance.total = total
        instance.total_price = total_price
        instance.active = True
        instance.save()



@receiver(post_save, sender=Orders)
def seles_update(sender, instance, created, **kwargs):
      obj, _ = Sales.objects.get_or_create(order=instance)
      obj.amount = instance.total_price
      obj.save()
        