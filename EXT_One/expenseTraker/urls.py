from django.contrib import admin
from django.urls import path
from .views import index, editExpense, deleteExpense

urlpatterns = [
    path('', index,name='index'),
    path('edit/<int:id>',editExpense,name="edit"),
    path('delete/<int:id>',deleteExpense,name='delete')
]