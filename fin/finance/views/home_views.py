from django.shortcuts import render, redirect
from ..forms import UserRegistrationForm


def home(request):
    return render(request, 'finance/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form
                                  .cleaned_data['password1'])
            new_user.save()
            return redirect('finance:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'finance/account/register.html', {'form': form})
