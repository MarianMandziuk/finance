from django.shortcuts import render
from ..forms import ReportForm
from ..models import Transaction, Category
from django.db.models import Sum
from django.contrib.auth.decorators import login_required


import json
import datetime


@login_required
def report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            if 'pie' in request.POST:
                return render(request,
                              'finance/report/report_pie.html',
                              generate_pie_data(form, request))
            elif 'line' in request.POST:
                return render(request,
                              'finance/report/report_line.html',
                              generate_line_data(form, request))
    else:
        form = ReportForm()
    return render(request, 'finance/report/report.html', {'form': form})


def generate_pie_data(form, request):
    form_fields = form.cleaned_data
    transactions = Transaction.objects.filter(user=request.user,
                                              date__range=(form_fields['start_date'], form_fields['end_date']))\
                                      .filter(type_operation=form_fields['type_operation'])
    categories = Category.objects.filter(user=request.user).all()
    data_for_line = []
    for category in categories:
        total_sum = 0
        for transaction in transactions.filter(category=category):
            total_sum += float(transaction.total)
        data_for_line.append({'name': category.name, 'y': total_sum})

    context = dict()
    context['data'] = json.dumps(data_for_line)
    context['data_category_sum'] = data_for_line
    context['start_date'] = form_fields['start_date']
    context['end_date'] = form_fields['end_date']
    context['total_sum'] = sum(d['y'] for d in data_for_line)
    return context


def generate_line_data(form, request):
    form_fields = form.cleaned_data
    transactions = Transaction.objects.filter(user=request.user,
                                              date__range=(form_fields['start_date'], form_fields['end_date'])) \
                                      .filter(type_operation=form_fields['type_operation'])
    data_for_line = []
    sum_by_dates = transactions.values('date').annotate(data_sum=Sum('total'))
    dict_sum_by_dates = {v['date']: float(v['data_sum']) for v in sum_by_dates}
    date1 = form_fields['start_date']
    date2 = form_fields['end_date']
    day = datetime.timedelta(days=1)
    while date1 <= date2:
        if date1 not in dict_sum_by_dates.keys():
            data_for_line.append(0)
        else:
            data_for_line.append(dict_sum_by_dates[date1])
        date1 = date1 + day

    data = {'name': 'money', 'data': data_for_line}
    context = dict()
    context['data'] = json.dumps(data)
    context['start_date'] = form_fields['start_date']
    context['end_date'] = form_fields['end_date']
    context['start_date_format'] = form_fields['start_date'].strftime('%Y, %m, %d')
    return context
