from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class job(models.Model):
    company = models.CharField(max_length=150, null=True, blank=True)
    job_title = models.CharField(max_length=150, null=True, blank=True)
    status = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.company


class subscribe(models.Model):
    job_title = models.CharField(max_length=150, null=True, blank=True)
    status = models.CharField(max_length=150, null=True, blank=True)


class Userverify(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    verify = models.BooleanField(default=False)



class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    biodata = models.CharField(max_length=50, null=True, blank=True)



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=200, null=True,blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)




class Chat(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"




    
