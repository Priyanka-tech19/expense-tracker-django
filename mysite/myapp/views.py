from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExpenseForm
from .models import Expense
import datetime
from django.db.models import Sum
from django.contrib.auth.decorators import login_required


# INDEX VIEW – Show and Add Expenses
@login_required
def index(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Link to logged-in user
            expense.save()
            return redirect('index')
    else:
        form = ExpenseForm()

    # Filter all data by the logged-in user
    user_expenses = Expense.objects.filter(user=request.user)
    total_expenses = user_expenses.aggregate(Sum('amount'))

    today = datetime.date.today()

    last_year = today - datetime.timedelta(days=365)
    yearly_sum = user_expenses.filter(date__gt=last_year).aggregate(Sum('amount'))

    last_month = today - datetime.timedelta(days=30)
    monthly_sum = user_expenses.filter(date__gt=last_month).aggregate(Sum('amount'))

    last_week = today - datetime.timedelta(days=7)
    weekly_sum = user_expenses.filter(date__gt=last_week).aggregate(Sum('amount'))

    daily_sums = user_expenses.values('date').order_by('date').annotate(sum=Sum('amount'))
    categorical_sums = user_expenses.values('category').order_by('category').annotate(sum=Sum('amount'))

    return render(request, 'myapp/index.html', {
        'expense_form': form,
        'expenses': user_expenses,
        'total_expenses': total_expenses,
        'yearly_sum': yearly_sum,
        'monthly_sum': monthly_sum,
        'weekly_sum': weekly_sum,
        'daily_sums': daily_sums,
        'categorical_sums': categorical_sums
    })


#  EDIT VIEW – Only your own expenses
@login_required
def edit(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    form = ExpenseForm(instance=expense)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')

    return render(request, 'myapp/edit.html', {
        'expense_form': form,
        'expense': expense
    })


#  DELETE VIEW – Only your own expenses
@login_required
def delete(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    if request.method == 'POST' and 'delete' in request.POST:
        expense.delete()
    return redirect('index')
