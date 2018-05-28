"""urls"""

from django.urls import path
from . import views

app_name = "blockchain"

urlpatterns = [
    path('', views.index, name="index"),
    path('transactions/', views.transactions_index, name="transactions_index"),
    path('new-wallet', views.generate_wallet, name="generate_wallet"),
    path('new-transaction/', views.make_transaction, name="make_transaction"),
    path('generate-transaction/', views.generate_transaction, name="generate_transaction"),
    path('view-transaction/', views.view_transaction, name="view_transaction"),
]

