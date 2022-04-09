from django.urls import path
from . import views

urlpatterns = [
  path('transaction/', views.transaction, name="transaction"),
  path('blockchain/', views.blockchain, name="blockchain"),
  path('blockchain/<str:pk>/', views.block_detail, name="block_detail"),
  path('validate/', views.validate_block, name="validate_block"),
]