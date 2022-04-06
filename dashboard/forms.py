from django import forms
from .models import *

class TransactionForm(forms.ModelForm):
  class Meta:
    model = RekodHarga

    fields = [
      'company_name_buy',
      'item_type',
      'quantity',
      'unit_of_measurement',
      'purchase_price',
    ]

    labels = {
      'company_name_buy': 'Syarikat Pembeli',
      'item_type': 'Jenis Barang',
      'quantity': 'Kuantiti',
      'unit_of_measurement': 'Unit jualan',
      'purchase_price': 'Harga beli (RM)',
    }

  def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
          if name == 'unit_of_measurement':
            field.widget.attrs.update({'class': 'form-select mb-3'})
          else:
            field.widget.attrs.update({'class': 'form-control mb-3'})
        