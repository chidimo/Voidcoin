"""urls"""

from django.urls import path
from . import views

app_name = "blockchain"

urlpatterns = [
    path('', views.index, name="index"),
    path('transactions/index/', views.transactions_index, name="transactions_index"),
    path('transactions/next-block/', views.transactions_destined_for_next_block, name="transactions_destined_for_next_block"),
    path('transactions/anon-user/', views.transaction_anon, name="transaction_anon"),
    path('transactions/auth-user/', views.transaction_auth_user, name="transaction_auth_user"),
    path('block/detail/<str:index>/', views.block_detail, name="block_detail"),
    path('block/mine/', views.mine, name="mine"),
    path('nodes/index/', views.node_index, name="node_index"),
    path('nodes/register/', views.register_nodes, name="register_nodes"),
    path('nodes/resolve/', views.consensus, name="consensus"),
]

