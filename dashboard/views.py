import json
import hashlib
import base64
from ecdsa import BadSignatureError, SECP256k1, SigningKey, VerifyingKey

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import *
import json
from .blockchain import Blockchain


@login_required(login_url="login")
def transaction(request):
  profile = request.user.profile
  name = request.user.first_name
  email = request.user.email
  form_transaction = TransactionForm(instance=profile)
  
  
  
  
  if request.method == "POST" and 'button1' in request.POST:
    form = TransactionForm(request.POST)
    if form.is_valid():
      rekodharga = form.save(commit=False)
      rekodharga.owner = profile
      rekodharga.save()
      newblock = create_block(rekodharga, profile)
      rekodharga.data_hash = newblock
      rekodharga.save()
      return redirect('transaction')

  record_list = profile.rekodharga_set.all()
  context = {
    'record_list' : record_list,
    'form_transaction' : form_transaction,
    'name': name,
    'email': email,
  }
  return render(request, 'dashboard/transaction.html', context)


def create_block(rekodharga, profile):
  previous_block = RekodBlokchain.objects.latest('timestamp')
  # Get from the user profile the public and private key
  vk_string = profile.public_key   # signing key
  sk_string = profile.private_key    # verifying key
  
  
  # Store all transaction information into dict
  temp_dict = {
    'company_name_buy': rekodharga.company_name_buy,
    'item_type': rekodharga.item_type,
    'quantity': rekodharga.quantity,
    'purchase_price': rekodharga.purchase_price,
  }

  # Get previous hash from previous block
  prev_hash = previous_block.hash_id

  encoded_data = json.dumps(temp_dict).encode()
  # Convert encoded data to data hash value and store in block
  data_hash = hashlib.sha256(encoded_data).hexdigest()

  # Signing the block using SECP256k1 elliptic curve
  sk = SigningKey.from_string(sk_string, curve=SECP256k1)
  vk = VerifyingKey.from_string(vk_string, curve=SECP256k1)

  # Get the digital singature and store value in block
  digital_signature = sk.sign(encoded_data)

  # Get previous proof from pervious block
  previous_proof = previous_block.nonce

  # Get the proof of work for this block
  nonce, hash_id = _proof_of_work(previous_proof, data_hash)

  newblock = RekodBlokchain.objects.create(
      prev_hash = prev_hash,
      data_hash = data_hash,
      data_signature = digital_signature,
      public_key = vk_string,
      nonce = nonce,
      hash_id = hash_id,
      flag_status= False
    )
  
  return newblock
  

def _to_digest(
        new_proof: int, previous_proof: int, data: str
    ) -> bytes:
        to_digest = str(new_proof ** 2 - previous_proof ** 2 + 2) + data
        # It returns an utf-8 encoded version of the string
        return to_digest.encode()


def _proof_of_work(previous_proof: str,  data: str) -> int:
        new_proof = 1
        check_proof = False
        hash_id = ''
        while not check_proof:
            to_digest = _to_digest(new_proof, previous_proof, data)
            hash_operation = hashlib.sha256(to_digest).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
                hash_id = hash_operation
            else:
                new_proof += 1

        return new_proof, hash_id


@login_required(login_url="login")
def blockchain(request):
  # RekodBlokchain.objects.all().delete()
  # Blockchain universal rekod asing
  profile = request.user.profile
  name = request.user.first_name
  email = request.user.email
  recordblockchain_list = RekodBlokchain.objects.all()
  print(recordblockchain_list)
  context = {
    'recordblockchain_list' : recordblockchain_list,
    'name': name,
    'email': email,
  }
  return render(request, 'dashboard/blockchain.html', context)
  
@login_required(login_url="login")
def block_detail(request, pk=None):
  
  profile = request.user.profile
  name = request.user.first_name
  email = request.user.email
  try:
    detail_block = RekodBlokchain.objects.get(id=pk)
  except ObjectDoesNotExist:
    print("Error!")
  # print(block.hash_id)
  context = {
    'detail_block' : detail_block,
    'name': name,
    'email': email,
  }
  return render(request, 'dashboard/blockchain_detail.html', context)

@login_required(login_url="login")
def validate_block(request):
  profile = request.user.profile
  name = request.user.first_name
  email = request.user.email
  # vk_string = profile.public_key
  # Queryset for rekod harga
  listRecord = RekodHarga.objects.all()
  # Queryset for recordblokchain
  recordblockchain_queryset = RekodBlokchain.objects.all()
  print(recordblockchain_queryset)
  print("\n")
  # Change recordblokchain queryset to list
  recordblockchain_list = list(recordblockchain_queryset)
  # Remove genisis block from the list
  recordblockchain_list.pop(0)

  index = 0
  for x in recordblockchain_list:
    status = True
    id = x.id
    for y in listRecord:
      temp_dict = {
      'company_name_buy': y.company_name_buy,
      'item_type': y.item_type,
      'quantity': y.quantity,
      'purchase_price': y.purchase_price,
      }
      encoded_data = json.dumps(temp_dict).encode()
      data_hash = hashlib.sha256(encoded_data).hexdigest()
      print("Comparing " + str(data_hash) + " with " + x.data_hash)
      if data_hash == x.data_hash:
        vk = VerifyingKey.from_string(x.public_key, curve=SECP256k1)
        try:
          if vk.verify(x.data_signature, encoded_data):
            status = False
            break
        except BadSignatureError:
          print(data_hash)
          print("Bad Signature!\n")
      # if sign_status:
      #   status = False
      #   break
    if status:
      change_flag_status(id, status)
      print("Block #" + str(index + 2) + " data has changed")
    else:
      change_flag_status(id, status)
      print("Block #" + str(index + 2) + " still maintain the same")
    index += 1
  
  recordblockchain_list = RekodBlokchain.objects.all()
  context = {
    'recordblockchain_list' : recordblockchain_list,
    'name': name,
    'email': email,
  }
  return render(request, 'dashboard/blockchain.html', context)

def change_flag_status(id, status):
  blok = RekodBlokchain.objects.get(id=id)
  blok.flag_status = status
  blok.save()