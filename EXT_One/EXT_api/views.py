import datetime

from django.http import JsonResponse
from django.db.models import Sum
from django.shortcuts import render
from expenseTraker.models import Expense
from EXT_api.serializer import Category_Spent_Serializer

def calculate_totalexpense_bymonth(curr_year,uid):
    months = ["Jan","Feb","Mar","Apr","May",'Jun',"Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    months_totals = {}
    for num,month in zip(range(1,13),months):
        month_total = Expense.objects.filter(date__month=num,user_id=uid).aggregate(Sum('amount',default=0))['amount__sum']

        months_totals[month] = month_total
    return months_totals

def calculate_spend_per_category(uid,curr_day,curr_month,curr__year):
    try:
        category_totals_today = Expense.objects.filter(user_id=uid,date__day=curr_day,date__month=curr_month,date__year=curr__year).values('category').order_by('category').annotate(sum=Sum('amount'))
    except:
        category_totals_today = {}
    print(category_totals_today.values())
    return category_totals_today
# Create your views here.

def users_totals_permonth(request,uid):
    total_per_months = calculate_totalexpense_bymonth(2024,uid)
    return JsonResponse(total_per_months)

def user_spend_by_category(request,uid):
    curr_day = datetime.date.today().day
    curr_month = datetime.date.today().month
    curr_year = datetime.date.today().year
    spend_perCategory = calculate_spend_per_category(uid,curr_day,curr_month,curr_year)

    return JsonResponse(Category_Spent_Serializer(spend_perCategory))

def user_calendar_data(request,uid):
    calendar_total_per_day = Expense.objects.filter(user_id=uid).values('date').order_by('date').annotate(sum=Sum('amount'))

    data = []
    for day in calendar_total_per_day:

        data.append({
            'title':"Total Spend " + str(day['sum']) + "$",
            'start': day['date'],
            'list-item': "matilda"
        })



    return JsonResponse(data,safe=False)
