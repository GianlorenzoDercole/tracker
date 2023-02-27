from django.shortcuts import render, redirect
from .forms import ExpenseForm
from .models import Expense
import datetime
from django.db.models import Sum
# Create your views here.

def index(request):
    # make form funtional
    if request.method =="POST":
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()
    expenses = Expense.objects.all()
    total_expenses = expenses.aggregate(Sum('amount'))
    # calculate expenses for 365 days
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data = Expense.objects.filter(date__gt=last_year)
    yearly_sum = data.aggregate(Sum('amount'))

        # calculate expenses for 30 days
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    data = Expense.objects.filter(date__gt=last_month)
    monthly_sum = data.aggregate(Sum('amount'))

        # calculate expenses for 7 days
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    data = Expense.objects.filter(date__gt=last_week)
    weekly_sum = data.aggregate(Sum('amount'))

    daily_sums = Expense.objects.filter().values('date').order_by('date').annotate(sum=Sum('amount'))

    expense_form = ExpenseForm()
    return render(request,'myapp/index.html',{'expense_form':expense_form,'expenses':expenses,'total_expenses':total_expenses,'yearly_sum':yearly_sum,'monthly_sum':monthly_sum,'weekly_sum':weekly_sum,'daily_sums':daily_sums})




def edit(request,id):
    # tell expense form on edit view what data to show
    expense = Expense.objects.get(id=id)
    expense_form = ExpenseForm(instance=expense)
    # update new data for expense
    if request.method =='POST':
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(request.POST,instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')

    return render(request,'myapp/edit.html',{'expense_form':expense_form})


def delete(request,id):
    if request.method =="POST" and 'delete' in request.POST:
        expense = Expense.objects.get(id=id)
        expense.delete()
    return redirect('index')
