import datetime

from django.db.models import Sum
from django.shortcuts import render, redirect
from .forms import ExpenseForm
from .models import Expense

months_key = "144025036146"

def calculate_expenses(curr_day,curr_month,curr_year,curr_day_ofweek):
#Calculates the Total amount of expenses in the current month
    expenses_this_month = Expense.objects.filter(date__month=curr_month, date__year=curr_year).aggregate(Sum('amount'))

#Calculate the total amount difference betwwen this month curr_mont and the past month.
    expenses_past_month = Expense.objects.filter(date__year=curr_year,
                                                 date__gte=datetime.date(curr_year,(curr_month-1),1),
                                                 date__lte=datetime.date(curr_year,curr_month,1))\
                                                .aggregate(Sum('amount'))
    curr_month_vs_last_month = expenses_this_month['amount__sum'] - expenses_past_month['amount__sum']
# Calculates the Total amount of expenses in the current week
    total_expense_week = Expense.objects.filter(date__gte=datetime.date(curr_year, curr_month, (curr_day - curr_day_ofweek + 1))).aggregate(Sum('amount'))

# Calculate the expenses compared to last week
    total_expense_lastweek = Expense.objects.filter(date__gte=datetime.date(curr_year, curr_month, (curr_day - (curr_day_ofweek) - 6)),
                                                    date__lte=datetime.date(curr_year, curr_month, (curr_day - curr_day_ofweek))).aggregate(Sum('amount'))
    curr_week_vs_last_week = total_expense_week['amount__sum'] - total_expense_lastweek['amount__sum']
    print(curr_week_vs_last_week)
# Calculates the Total amount of expenses in the current day
    total_expense_today = Expense.objects.filter(date__day=curr_day).aggregate(Sum('amount'))


# Calculates the Total amount of expenses separated by category in current day
    category_totals_today = Expense.objects.filter(date__day=curr_day).values('category').order_by('category').annotate(sum=Sum('amount'))

# Calculate the total spended by category this week.

#collects the expenses from yesterday and it calculates the difference
    total_expense_yesterday = Expense.objects.filter(date__day=curr_day - 1).aggregate(Sum('amount'))
    if total_expense_yesterday['amount__sum'] is None:
        total_expense_yesterday['amount__sum'] = 0
    if total_expense_today['amount__sum'] is None:
        total_expense_today['amount__sum'] = 0
    print(category_totals_today)
    today_vs_yesterday = total_expense_today['amount__sum'] - total_expense_yesterday['amount__sum']

    return {'expenses_this_month':expenses_this_month,
            'total_expense_week':total_expense_week,
            'total_expense_today':total_expense_today,
            'today_vs_yesterday':today_vs_yesterday,
            'category_totals_today':category_totals_today,
            'curr_month_vs_last_month':curr_month_vs_last_month,
            'curr_week_vs_last_week':curr_week_vs_last_week
            }
# Create your views here.
def index(request):
    curr_day   = datetime.date.today().day
    curr_month = datetime.date.today().month
    curr_year  = datetime.date.today().year
    curr_day_ofweek = ( int((curr_year%1100)%100/4) + curr_day + int(months_key[curr_month]) + (curr_year%1100)%100 + 5) % 7
    print(curr_day_ofweek)
    if request.POST:
        expense = ExpenseForm(request.POST)
        expense.save()
    expense_form = ExpenseForm()
    expense_list = Expense.objects.all().order_by('date')
    expense_totals = calculate_expenses(curr_day,curr_month,curr_year,curr_day_ofweek)
    
    return render(request,"expenseTraker/index.html",{'expense_form':expense_form,
                                                      'expense_list':expense_list,
                                                      'total_expense_month': expense_totals['expenses_this_month'],
                                                      'curr_month_vs_last_month':expense_totals['curr_month_vs_last_month'],
                                                      'total_expense_week': expense_totals['total_expense_week'],
                                                      'curr_week_vs_last_week':expense_totals['curr_week_vs_last_week'],
                                                      'total_expense_today':expense_totals['total_expense_today'],
                                                      'today_vs_yesterday':expense_totals['today_vs_yesterday'],
                                                      'category_totals_today':expense_totals['category_totals_today']
                                                      })


def editExpense(request,id):

    expense = Expense.objects.get(id=id)
    expense_form = ExpenseForm(instance=expense)

    if request.POST:

        form = ExpenseForm(request.POST,instance=expense)
        if form.is_valid():
            form.save()
            return redirect(index)
    return render(request,"expenseTraker/editExpense.html",{'expense_form':expense_form})

def deleteExpense(request,id):
    expense = Expense.objects.get(id=id)
    expense.delete()
    return redirect(index)