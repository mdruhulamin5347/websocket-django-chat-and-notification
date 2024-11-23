from  django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save,sender=job)
def job_signals(sender, instance, **kwargs):
    subscribe.objects.create(job_title=instance.job_title,status =instance.status)

# post_save.connect(job_signals, sender=job)


@receiver(post_save, sender=User)
def user_verify(sender,instance, created , **kwargs):
    obj, created = Userverify.objects.get_or_create(user=instance)
    if not obj.verify:
        obj.verify = True
        obj.save()

    if created:
        subject = f'Hi {instance.username}'  # Corrected to use username or another user attribute
        message = 'Your account has been successfully created. Thanks for creating an account!'
        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = instance.email

        send_mail(
            subject,
            message,
            email_from,
            [email_to],  # Recipient list should be a list
            fail_silently=False,
        )




@receiver(post_save, sender=User)
def Profile_create(sender, instance , **kwargs):
    obj , _ = Profile.objects.get_or_create(user=instance)
    obj.biodata = "i am a backend developer"
    obj.save()