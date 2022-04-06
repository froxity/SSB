from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile
from dashboard .models import RekodHarga, RekodBlokchain
from django.core.mail import send_mail
from django.conf import settings

from Crypto.PublicKey import RSA

def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        key = RSA.generate(2048)
        p_key = key.public_key().exportKey("PEM")
        new_p_key = p_key[28:-26]
        priv_key = key.exportKey("PEM")
        new_priv_key = priv_key[33:-41]
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            first_name = user.first_name,
            last_name = user.last_name,
            public_key = new_p_key,
            private_key = new_priv_key,
        )


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.first_name
        user.last_name = profile.last_name
        user.username = profile.username
        user.email = profile.email
        user.save()

def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()

post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)