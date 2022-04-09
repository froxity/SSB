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
  # Queryset for rekod harga
  listRecord = RekodHarga.objects.all()
  # Queryset for recordblokchain
  recordblockchain_queryset = RekodBlokchain.objects.all()
  # Change recordblokchain queryset to list
  recordblockchain_list = list(recordblockchain_queryset)
  # Remove genisis block from the list
  recordblockchain_list.pop(0)
  
  index = 0
  for x in listRecord:
    status = True
    id = None
    for y in recordblockchain_list:
      id = y.id #a Get Id from record blockchain
      temp_dict = {
      'company_name_buy': x.company_name_buy,
      'item_type': x.item_type,
      'quantity': x.quantity,
      'purchase_price': x.purchase_price,
      }
      encoded_data = json.dumps(temp_dict).encode()
      data_hash = hashlib.sha256(encoded_data).hexdigest()
      if data_hash == y.data_hash:
        status = False
        change_flag_status(id, status)
        print("Block #" + str(index + 2) + " still maintain the same")
        break
      
    change_flag_status(id, status)
    print("Block #" + str(index + 2) + " data has changed")
    index += 1
  
  """ FOR REFERENCES
  # Put all data hash for all record blockchain into another list
  tempDataHashRecordBlockchain = []
  tempIDRecordBlockchain = []
  for x in recordblockchain_list:
    tempDataHashRecordBlockchain.append(x.data_hash)
    tempIDRecordBlockchain.append(x.id)
  print(tempDataHashRecordBlockchain)
  # Put all list_record encoded data into temporary list
  tempDataHashRecordTransaction = []
  for x in listRecord:
    temp_dict = {
      'company_name_buy': x.company_name_buy,
      'item_type': x.item_type,
      'quantity': x.quantity,
      'purchase_price': x.purchase_price,
    }
    encoded_data = json.dumps(temp_dict).encode()
    data_hash = hashlib.sha256(encoded_data).hexdigest()
    tempDataHashRecordTransaction.append(data_hash)
  # Check is recordchain new data hash encoded is same inside the 
  # tempDataHashRecordBlockchain
  index = 0
  for x in tempDataHashRecordTransaction:
    if x in tempDataHashRecordBlockchain:
      id = tempIDRecordBlockchain[index]
      status = False # Data has NOT changed
      change_flag_status(id, status)
      print("Block #" + str(index + 2) + " still maintain the same")
    else:
      id = tempIDRecordBlockchain[index]
      status = True # Data has changed
      change_flag_status(id, status)
      print("Block #" + str(index + 2) + " data has changed")
    index+=1
  """
  
  
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