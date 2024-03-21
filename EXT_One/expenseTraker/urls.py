from django.contrib import admin
from django.urls import path
from .views import index, editExpense, deleteExpense, sign_up,Log_out,calendar_View,day_view,Profile

urlpatterns = [
    path('', index,name='index'),
    path('calendar/',calendar_View,name="calendar"),
    path('day_view/<str:date>',day_view,name="day_view"),
    path('edit/<int:id>',editExpense,name="edit"),
    path('delete/<int:id>',deleteExpense,name='delete'),
    path('sign-up', sign_up, name='sign-up'),
    path('accounts/logout',Log_out,name='log_out'),
    path('profile/<int:uid>',Profile,name='Profile')

]