"""urls"""

from django.urls import path
from . import views

app_name = "blockchain"

urlpatterns = [
    path('', views.index, name="index"),
    path('wallet/new/', views.generate_wallet, name="generate_wallet"),
    path('wallet/view/', views.wallet_detail, name="wallet_detail"),
    path('transactions/', views.transactions_index, name="transactions_index"),
    path('transactions/new/', views.make_transaction, name="make_transaction"),
    path('transactions/initiate/', views.initiate_transaction, name="initiate_transaction"),
    path('transactions/validate/', views.validate_and_block_transaction, name="validate_and_block_transaction"),
    path('transaction/detail/', views.transaction_detail, name="transaction_detail"),
    path('block/detail/<str:index>/', views.block_detail, name="block_detail"),
    path('block/mine/', views.mine, name="mine"),
    path('nodes/index/', views.node_index, name="node_index"),
    path('nodes/register/', views.register_nodes, name="register_nodes"),
    path('nodes/resolve/', views.consensus, name="consensus"),
]

