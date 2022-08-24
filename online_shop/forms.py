from django import forms
from django.core.exceptions import ValidationError

class LogInForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control mb-3'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))
 
class SignUpForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control mb-3'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))
    confirm_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                print('password error')
                raise ValidationError(('Password confirmation not the same'), code='unequal_password')