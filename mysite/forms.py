from django import forms
from django.contrib import auth


class LoginFrom(forms.Form):
    username = forms.CharField(label="用户名", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("用户名或密码错误！")
        else:
            self.cleaned_data['user'] = user

        return self.cleaned_data
