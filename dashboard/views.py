from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
import json
from .blockchain import Blockchain
# import blockchain
import hashlib
import base64
import ecdsa
# Create your views here.



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
  print(previous_block)
  pb_key = profile.public_key
  priv_key = profile.private_key
  temp_dict = {
      'company_name_buy': rekodharga.company_name_buy,
      'item_type': rekodharga.item_type,
      'quantity': rekodharga.quantity,
      # 'unit_of_measurement': x.unit_of_measurement,
      'purchase_price': rekodharga.purchase_price,
    }
  prev_hash = previous_block.hash_id
  encoded_data = json.dumps(temp_dict).encode()
  data_hash = hashlib.sha256(encoded_data).hexdigest()

  # SECP256k1 is the Bitcoin elliptic curve
  sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) 
  digital_signature = sk.sign(encoded_data)
  previous_proof = previous_block.nonce
  nonce, hash_id = _proof_of_work(previous_proof, data_hash)

  newblock = RekodBlokchain.objects.create(
      prev_hash = prev_hash,
      data_hash = data_hash,
      data_signature = digital_signature,
      public_key = pb_key,
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
  context = {
    'recordblockchain_list' : recordblockchain_list,
    'name': name,
    'email': email,
  }
  return render(request, 'dashboard/blockchain.html', context)
  # record_list = profile.rekodharga_set.all()
  # bc = Blockchain()
  # for x in record_list:
  #   temp_dict = {
  #     'company_name_buy': x.company_name_buy,
  #     'item_type': x.item_type,
  #     'quantity': x.quantity,
  #     # 'unit_of_measurement': x.unit_of_measurement,
  #     'purchase_price': x.purchase_price,
  #   }
  #   encoded_data = json.dumps(temp_dict).encode()
  #   data_hash = hashlib.sha256(encoded_data).hexdigest()
  #   bc.mine_block(data_hash)
  # blockchain_dict = bc.chain
  # for x in bc.chain:
  #   RekodBlokchain.objects.create(
  #     prev_hash = x['previous_hash'],
  #     data_hash = x['data'],
  #     data_signature = "1a2fc26dc7ea5a2a4748b7cb2b1ef193d96ab2c99f93092f69e63075b28d1278",
  #     public_key = '20aab1f98b65f79fc05124309b891903eac6545c31eacef17ca5693597e9531e',
  #     nonce = x['proof'],
  #     hash_id = x['hash_id'],
  #     owner = profile,
  #   )
  
@login_required(login_url="login")
def block_detail(request, pk, block_no):
  profile = request.user.profile
  name = request.user.first_name
  email = request.user.email
  detail_block = RekodBlokchain.objects.get(id=pk)
  # print(block.hash_id)
  context = {
    'detail_block' : detail_block,
    'block_no' : block_no,
    'name': name,
    'email': email,
  }
  return render(request, 'dashboard/blockchain_detail.html', context)

@login_required(login_url="login")
def validate_block(request):
  profile = request.user.profile
  name = request.user.first_name
  email = request.user.email

  list_record = RekodHarga.objects.all()
  # Queryset for recordblokchain
  recordblockchain_queryset = RekodBlokchain.objects.all()
  # Change queryset to list
  recordblockchain_list = list(recordblockchain_queryset)
  recordblockchain_list.pop(0)
  # print(list_record)
  # print(recordblockchain_list)
  bc = Blockchain()
  index = 2 #index starting block no 2 
  for x in list_record:
    flag = True
    for y in recordblockchain_list:
      temp_dict = {
        'company_name_buy': x.company_name_buy,
        'item_type': x.item_type,
        'quantity': x.quantity,
        'purchase_price': x.purchase_price,
      }
      encoded_data = json.dumps(temp_dict).encode()
      data_hash = hashlib.sha256(encoded_data).hexdigest()
      if data_hash == y.data_hash:
        print("Block #" + str(index) + " still maintain the same")
        flag = False
        break
    if flag:
      change_flag_status(y.id)
      print("Block #" + str(index) + " data has changed")
    index = index + 1
  
  recordblockchain_list = RekodBlokchain.objects.all()
  context = {
    'recordblockchain_list' : recordblockchain_list,
    'name': name,
    'email': email,
  }
  return render(request, 'dashboard/blockchain.html', context)
  # return redirect('blockchain')

def change_flag_status(id):
  blok = RekodBlokchain.objects.get(id=id)
  blok.flag_status = True
  blok.save()