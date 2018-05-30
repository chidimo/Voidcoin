"""urls"""

from django.urls import path
from . import views

app_name = "blockchain"

urlpatterns = [
    path('', views.index, name="index"),
    path('wallet/new/', views.generate_wallet, name="generate_wallet"),
    path('transactions/chain/', views.transactions_index, name="transactions_index"),
    path('transactions/next-block/', views.transactions_destined_for_next_block, name="transactions_destined_for_next_block"),
    path('transactions/anon-user/', views.transaction_anon, name="transaction_anon"),
    path('transactions/auth-user/', views.transaction_auth_user, name="transaction_auth_user"),
    path('transactions/validate/', views.validate_and_block_transaction, name="validate_and_block_transaction"),
    path('block/detail/<str:index>/', views.block_detail, name="block_detail"),
    path('block/mine/', views.mine, name="mine"),
    path('nodes/index/', views.node_index, name="node_index"),
    path('nodes/register/', views.register_nodes, name="register_nodes"),
    path('nodes/resolve/', views.consensus, name="consensus"),
    path('edit-alias/', views.edit_alias, name="edit_alias"),
]

