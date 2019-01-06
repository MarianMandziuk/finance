from django import forms
from .models import Transaction
from bootstrap_datepicker_plus import DatePickerInput
from django.contrib.auth.models import User


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('category', 'type_operation', 'total', 'date', 'description')
        widgets = {
            'date': DatePickerInput(),
        }


class ReportForm(forms.Form):
    start_date = forms.DateField(widget=DatePickerInput())
    end_date = forms.DateField(widget=DatePickerInput())
    type_operation = forms.ChoiceField(choices=Transaction.CHOICES)

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        start_date = self.cleaned_data['start_date']
        if end_date < start_date:
            raise forms.ValidationError("End date must be greater when end date!")

        return end_date


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']