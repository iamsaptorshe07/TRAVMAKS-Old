from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from homeApp.email_sender import *

# Create your models here.
class ContactMessage(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=100)
    message = models.TextField()


@receiver(post_save,sender=ContactMessage)
def contactMessager(sender,instance,created,*args,**kwargs):
    if created:
        contact = instance
        contactMessageSender(contact)