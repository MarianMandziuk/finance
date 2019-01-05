from django import forms
from .models import Transaction
from bootstrap_datepicker_plus import DatePickerInput


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('category', 'type_operation', 'total', 'date', 'description')
        widgets = {
            'date': DatePickerInput(),
        }