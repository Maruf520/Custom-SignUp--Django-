from django import forms
from django.contrib.auth import authenticate
# from  models import Account
from account.models import Account


class SignupForm(forms.ModelForm):
    password  = forms.CharField(widget=forms.PasswordInput(attrs={ 'placeholder': 'password (min 6 word)','class':'form-control','minLength':'6', 'maxLength':'10' }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs = {'placeholder':'confirm_password', 'class': 'form-control'}))
    class Meta:
        model = Account
        fields = ['username', 'email']
        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control'}),
            'email' : forms.EmailInput(attrs={ 'class': 'form-control' })
        } 

        def email(self):
            email = self.cleaned_data['email']
            query =  Account.objects.filter(email = email)
            if query.exists():
                raise forms.ValidationError(' Email has already registered')
            return email

        # def username(self):
        #     username = self.cleaned_data['username']
        #     query = self   
         


         
        def clean_confirm_password(self):
            password = self.cleaned_data['password']
            confirm_password = self.cleaned_data['confirm_password']
            if len(password) < 6:
                raise forms.ValidationError('password should be at least 6 length')
            if len(password) > 12:
                raise forms.ValidationError('password should be at most 12 length')
            if not any(char.isdigit() for char in password):
                raise forms.ValidationError('password must contain at least 1 digit')
            if not any(char.isupper() for char in password):
                raise forms.ValidationError('password must contain at least 1 upper letter')
            if not any(char.islower() for char in password):
                raise forms.ValidationError('password must contain at least 1 upper letter')
            if not any(symbol in password for symbol in ['~','!','#','$']):
                raise forms.ValidationError("use any of '~','!','#','$'")
            if not password or not confirm_password or password != confirm_password:
                raise forms.ValidationError('passwords are not matched')
            return confirm_password

        def save(self, commit = True):
            user = Account(
                username = self.cleaned_data['username'],
                email = self.cleaned_data['email']
            )

            user.set_password(self.cleaned_data['confirm_password'])
            if commit:
                user.save()
            return user    

