"""urls"""

from django.urls import path
from . import views

app_name = "blockchain"

urlpatterns = [
    path('', views.index, name="index"),
    path('new-wallet', views.generate_wallet, name="generate_wallet"),
    path('transactions/', views.transactions_index, name="transactions_index"),
    path('transactions/new/', views.make_transaction, name="make_transaction"),
    path('transactions/initiate/', views.initiate_transaction, name="initiate_transaction"),
    path('transactions/validate/', views.validate_and_block_transaction, name="validate_and_block_transaction"),
    path('transactions/view/', views.view_transaction, name="view_transaction"),
    path('transactions/get/', views.transactions_in_block, name="transactions_in_block"),
]

