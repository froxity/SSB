from django.db import models
import uuid
from user.models import Profile
# Create your models here.

class RekodHarga(models.Model):
  id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
  owner = models.ForeignKey(Profile,on_delete=models.CASCADE, null=True, blank=True)
  timestamp = models.DateTimeField(auto_now_add=True)
  company_name_buy = models.CharField(max_length=500)
  item_type = models.CharField(max_length=500)
  quantity = models.IntegerField(null=False, blank=False)
  unit_of_measurement = models.ForeignKey('UnitOfMeasurement', null=True, blank=True, on_delete=models.SET_NULL)
  purchase_price = models.IntegerField(null=False, blank=False)
  data_hash = models.ForeignKey('RekodBlokchain', null=True, blank=True, on_delete=models.SET_NULL)

  class Meta:
        ordering = ('timestamp',)
  
  def __str__(self):
    temp = str(self.owner) + ' | ' + str(self.id) + ' | ' + str(self.item_type)
    return temp

class RekodBlokchain(models.Model):
  id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
  # transaction_id = models.ForeignKey('RekodHarga', null=True, blank=True, on_delete=models.SET_NULL)
  # owner = models.ForeignKey(Profile,on_delete=models.CASCADE, null=True, blank=True)
  timestamp = models.DateTimeField(auto_now_add=True)
  prev_hash = models.CharField(max_length=300)
  data_hash = models.CharField(max_length=300)
  data_signature = models.BinaryField(null=True, blank=True)
  public_key = models.BinaryField(null=True, blank=True)
  nonce = models.IntegerField(null=False, blank=False)
  hash_id = models.CharField(max_length=300)
  flag_status = models.BooleanField(null=True, blank=False)

  class Meta:
        ordering = ('timestamp',)

  def __str__(self):
    return self.hash_id
  

class UnitOfMeasurement(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name