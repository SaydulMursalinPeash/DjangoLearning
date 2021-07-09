from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


def customer_profile(sender,instance,created,**kwargs):
    if created:
        if instance.is_superuser==True:
            group = Group.objects.get(name='Admin')

        else:
            group = Group.objects.get(name='Customer')
        instance.groups.add(group)
        Customer.objects.create(user=instance, name=instance.username, email=instance.email)

post_save.connect(customer_profile,sender=User)