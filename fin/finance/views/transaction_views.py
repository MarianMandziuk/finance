from django.shortcuts import render, redirect, get_object_or_404
from ..models import Transaction, Category
from django.views.generic import ListView
from django.contrib import messages
from ..forms import TransactionForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


TRANSACTION_SHOW = 10


class TransactionList(ListView):
    template_name = 'finance/transaction/list.html'
    queryset = Transaction.objects.all()[:10]
    context_object_name = 'transactions'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TransactionList, self).dispatch(request, *args, **kwargs)


@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.save()
            messages.success(request, 'Transaction "{}" was successfully created'
                                      .format(transaction.description))
            return redirect("finance:transaction_list")
    else:
        form = TransactionForm()
    categories = Category.objects.all()
    return render(request, 'finance/transaction/create_update.html', {'form': form,
                                                                      'categories': categories,
                                                                      'choices': Transaction.CHOICES})


@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.delete()
    messages.success(request, 'Transaction "{}" was successfully deleted'
                     .format(transaction.description))
    return redirect("finance:transaction_list")


@login_required
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            current_transaction = form.save(commit=False)
            current_transaction.save()
            messages.success(request, 'Transaction "{}" was successfully updated on {}'
                             .format(transaction.description, current_transaction.description))
            return redirect("finance:transaction_list")
    else:
        data = {'category': transaction.category,
                'type_operation': transaction.type_operation,
                'total': transaction.total,
                'date': transaction.date,
                'description': transaction.description}
        form = TransactionForm(initial=data)
    update = True
    return render(request, "finance/transaction/create_update.html", {
        'update': update,
        'form': form,
    })
