from ecdsa import SigningKey, VerifyingKey ,SECP256k1

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Profile
from dashboard .models import RekodHarga, RekodBlokchain
from django.core.mail import send_mail
from django.conf import settings


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        # Signing key = Private key
        sk = SigningKey.generate(curve=SECP256k1)
        # Change sk to_string and save as privateKey
        privateKey = sk.to_string()

        # Create Verifying key = Public key
        vk = sk.verifying_key
        # Change vk to_string and save as publicKey
        publicKey = vk.to_string()

        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            first_name = user.first_name,
            public_key = publicKey,
            private_key = privateKey,
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