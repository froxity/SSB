from django.db import models

# Create your models here.
from django.db import models
import uuid
from django.contrib.auth.models import User

class Profile(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    public_key = models.BinaryField(null=True, blank=True)
    private_key = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return str(self.user.username)
