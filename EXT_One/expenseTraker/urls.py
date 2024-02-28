from django.contrib import admin
from django.urls import path
from .views import index, editExpense, deleteExpense, sign_up,Log_out

urlpatterns = [
    path('', index,name='index'),
    path('edit/<int:id>',editExpense,name="edit"),
    path('delete/<int:id>',deleteExpense,name='delete'),
    path('sign-up', sign_up, name='sign-up'),
    path('accounts/logout',Log_out,name='log_out'),

]