from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import Expense

class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        exclude = ['user']
        fields = ('name', 'amount', 'category')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'pl-10 block w-full rounded-lg border-gray-300 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200',
                'placeholder': 'Enter expense name'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'pl-10 block w-full rounded-lg border-gray-300 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200',
                'placeholder': 'Enter amount',
                'step': '0.01'
            }),
            'category': forms.Select(attrs={
                'class': 'pl-10 block w-full rounded-lg border-gray-300 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200'
            })
        }

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'pl-10 block w-full rounded-lg border-gray-300 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'pl-10 block w-full rounded-lg border-gray-300 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200',
                'placeholder': 'Enter last name'
            }),
            'username': forms.TextInput(attrs={
                'class': 'pl-10 block w-full rounded-lg border-gray-300 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200',
                'placeholder': 'Choose a username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'pl-10 block w-full rounded-lg border-gray-300 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200',
                'placeholder': 'Enter your email'
            })
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # Add styling to password fields which are not in the widgets dict
        self.fields['password1'].widget.attrs.update({
            'class': 'pl-10 block w-full rounded-lg border-gray-300 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'pl-10 block w-full rounded-lg border-gray-300 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200',
            'placeholder': 'Confirm password'
        })