from django.contrib import admin
from django.urls import path, include
from EXT_api import views

urlpatterns = [
    path('get_user_chart_data/<int:uid>',views.users_totals_permonth),
    path('get_user_category_spend/<int:uid>',views.user_spend_by_category),
    path('calendar_data/<int:uid>/',views.user_calendar_data)
]