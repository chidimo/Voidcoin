"""urls"""

from django.urls import path
from . import views

app_name = "blockchain"

urlpatterns = [
    path('', views.index, name="index"),
    path('wallet/new/', views.generate_wallet, name="generate_wallet"),
    path('transactions/chain/', views.transactions_index, name="transactions_index"),
    path('transactions/next-block/', views.transactions_destined_for_next_block, name="transactions_destined_for_next_block"),
    path('transactions/initiate/', views.initiate_transaction, name="initiate_transaction"),
    path('transactions/initiate-and-verify/', views.initiate_and_verify_transaction, name="initiate_and_verify_transaction"),
    path('transactions/validate/', views.validate_transaction_and_add_it_to_block, name="validate_transaction_and_add_it_to_block"),
    path('block/detail/<str:index>/', views.block_detail, name="block_detail"),
    path('block/mine/', views.mine, name="mine"),
    path('nodes/index/', views.node_index, name="node_index"),
    path('nodes/register/', views.register_nodes, name="register_nodes"),
    path('nodes/resolve/', views.consensus, name="consensus"),
]

