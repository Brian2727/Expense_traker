import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect
from .forms import ExpenseForm, RegistrationForm
from .models import Expense
from django.contrib.auth import login,logout,authenticate

months_key = "144025036146"

def calculate_totalexpense_bymonth(curr_year,uid):
    months = ["Jan","Feb","Mar","Apr","May",'Jun',"Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    months_totals = {}
    for num,month in zip(range(1,13),months):
        month_total = Expense.objects.filter(date__month=num,user_id=uid).aggregate(Sum('amount',default=0))['amount__sum']

        months_totals[month] = month_total
    print(months_totals)
    return months_totals
def calculate_expenses(curr_day,curr_month,curr_year,curr_day_ofweek,uid):
#Calculates the Total amount of expenses in the current month
    try:
        expenses_this_month = Expense.objects.filter(user_id=uid,date__month=curr_month, date__year=curr_year).aggregate(Sum('amount',default=0))
    except:
        # If the expense filter fails then we set the amount sum to 0 sicne ther i sno expenses
        expenses_this_month = {'amount__sum':0}
#Calculate the total amount difference between this month curr_mont and the past month.
#Check That we have expenses last month
    try:
        expenses_past_month = Expense.objects.filter(user_id=uid,date__year=curr_year,
                                                 date__gte=datetime.date(curr_year,(curr_month-1),1),
                                                 date__lte=datetime.date(curr_year,curr_month,1))\
                                                .aggregate(Sum('amount',default=0))
    except:
        expenses_past_month  = {'amount__sum':0}
    curr_month_vs_last_month = expenses_this_month['amount__sum'] - expenses_past_month['amount__sum']

# Calculates the Total amount of expenses in the current week
    try:
        total_expense_week = Expense.objects.filter(user_id=uid,date__gte=datetime.date(curr_year, curr_month, (curr_day - curr_day_ofweek)),
                                              date__lte=datetime.date(curr_year, curr_month, (curr_day - curr_day_ofweek + 7))).aggregate(Sum('amount',default=0))
    except:
        total_expense_week = {'amount__sum':0}
# Calculate the expenses compared to last week
    try:
        total_expense_lastweek = Expense.objects.filter(user_id=uid,date__gte=datetime.date(curr_year, curr_month, (curr_day - (curr_day_ofweek) - 7)),
                                                    date__lte=datetime.date(curr_year, curr_month, (curr_day - curr_day_ofweek))).aggregate(Sum('amount',default=0))
    except:
        total_expense_lastweek = {'amount__sum':0}
    curr_week_vs_last_week = total_expense_week['amount__sum'] - total_expense_lastweek['amount__sum']

# Calculates the Total amount of expenses in the current day
    try:
        total_expense_today = Expense.objects.filter(user_id=uid,date__day=curr_day,date__month=curr_month,date__year=curr_year).aggregate(Sum('amount',default=0))
    except:
        total_expense_today = {'amount__sum':0}
#collects the expenses from yesterday and it calculates the difference
    try:
        total_expense_yesterday = Expense.objects.filter(user_id=uid,date__day=curr_day - 1).aggregate(Sum('amount',default=0))
    except:
        total_expense_yesterday = {'amount__sum':0}


    today_vs_yesterday = total_expense_today['amount__sum'] - total_expense_yesterday['amount__sum']

# Calculates the Total amount of expenses separated by category in current day
#no need to add a default value to this one since on the view we will not itterate ove the for loop
    try:
        category_totals_today = Expense.objects.filter(user_id=uid,date__day=curr_day,date__month=curr_month,date__year=curr_year).values('category').order_by('category').annotate(sum=Sum('amount'))
    except:
        category_totals_today = {}
# Calculate the total spended by category this week.



    return {'expenses_this_month':expenses_this_month,
            'total_expense_week':total_expense_week,
            'total_expense_today':total_expense_today,
            'today_vs_yesterday':today_vs_yesterday,
            'category_totals_today':category_totals_today,
            'curr_month_vs_last_month':curr_month_vs_last_month,
            'curr_week_vs_last_week':curr_week_vs_last_week
            }

def calculate_day_expenses(date,uid):
    sel_day_expenses = {}
    category_totals_selected_day = Expense.objects.filter(user_id=uid, date=date).values('category').annotate(sum=Sum('amount'))
    category_totals_selected_day = category_totals_selected_day.order_by('-sum')
    print(category_totals_selected_day)
    total_Expenses_selected_day = Expense.objects.filter(date=date, user_id=uid).annotate(sum=Sum('amount'))
    sel_day_expenses['category_totals_selected_day'] = category_totals_selected_day
    sel_day_expenses['total_Expenses_selected_day'] = total_Expenses_selected_day

    print(sel_day_expenses)
    return sel_day_expenses

# Create your views here--------------------------------------------------------------------------------------------------------------------.
def sign_up(request):
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user =  form.save()
            login(request,user)
            return redirect(index)
    else:
        form = RegistrationForm()

    return render(request,'registration/sign-up.html',{'form':form})

def Log_out(request):
    logout(request)
    return redirect(index)

def Profile(request,uid):

    return render(request,'expenseTraker/profile.html',{
        'uid':uid
    })
@login_required()
def index(request):
    user_id = request.user.id
    curr_day   = datetime.date.today().day
    curr_month = datetime.date.today().month
    curr_year  = datetime.date.today().year
    curr_day_ofweek = datetime.date.today().weekday() + 1 #( int((curr_year%1100)%100/4) + curr_day + int(months_key[curr_month]) + (curr_year%1100)%100 + 5) % 7
    print(f"current day of week {curr_day_ofweek}")
    calculate_totalexpense_bymonth(curr_year,user_id)
    #check for post request to save expense
    #Was having issues with this save function since from a form you do not initialize so you have to do a save with
    #comit - False to get the model back abd the add the user id and finally you can save this is only if done with a form
    if request.POST:
        expense = ExpenseForm(request.POST)
        post = expense.save(commit=False)
        post.user = request.user
        post.save()

    expense_form = ExpenseForm()

    expense_list = Expense.objects.filter(user=request.user,date__month=curr_month).order_by('date')

    #check if there is any expenses adding user id to get users expenses

    expense_totals = calculate_expenses(curr_day,curr_month,curr_year,curr_day_ofweek,user_id)
    months_totals = calculate_totalexpense_bymonth(uid=user_id,curr_year=curr_year)


    return render(request,"expenseTraker/index.html",{'expense_form':expense_form,
                                                      'expense_list':expense_list,
                                                      'total_expense_month': expense_totals['expenses_this_month'],
                                                      'curr_month_vs_last_month':expense_totals['curr_month_vs_last_month'],
                                                      'total_expense_week': expense_totals['total_expense_week'],
                                                      'curr_week_vs_last_week':expense_totals['curr_week_vs_last_week'],
                                                      'total_expense_today':expense_totals['total_expense_today'],
                                                      'today_vs_yesterday':expense_totals['today_vs_yesterday'],
                                                      'category_totals_today':expense_totals['category_totals_today'],
                                                      'months_totals':months_totals
                                                      })
@login_required()
def calendar_View(request):

    return render(request,"expenseTraker/calendarView.html")

@login_required()
def day_view(request,date):
    expense_form = ExpenseForm()
    if request.POST:
        expense = ExpenseForm(request.POST)
        post = expense.save(commit=False)

        post.user = request.user

        print(f"this is my post {post.save(date=date)}")
    expenses_metrics_today = calculate_day_expenses(date,request.user.id)
    expense_list = Expense.objects.filter(date=date,user_id=request.user.id)
    total_expense = expense_list.aggregate(sum=Sum('amount'))['sum']
    print(total_expense)
    return render(request,'expenseTraker/day_view.html',{
        'expense_form': expense_form,
        "expense_list":expense_list,
        "expense_by_category": expenses_metrics_today["category_totals_selected_day"],
        "total_expense": total_expense,
        "selected_day":date
    })

def editExpense(request,id):

    expense = Expense.objects.get(id=id)
    expense_form = ExpenseForm(instance=expense)

    if request.POST:

        form = ExpenseForm(request.POST,instance=expense)
        if form.is_valid():
            form.save()
            return render(request,"expenseTraker/editExpense.html",{'expense_form':expense_form})
    return render(request,"expenseTraker/editExpense.html",{'expense_form':expense_form})

def deleteExpense(request,id):
    expense = Expense.objects.get(id=id)
    expense.delete()
    return redirect(index)