from django import forms


class Login(forms.Form):
    user_name = forms.CharField(label='user_name', max_length=40)
    password = forms.CharField(label='password', max_length=40)


class Registration(forms.Form):
    user_name = forms.CharField(label='user_name', max_length=40)
    email = forms.CharField(label='email', max_length=40)
    password = forms.CharField(label='password', max_length=40)


class MakeBattle(forms.Form):
    name = forms.CharField(label='name', max_length=40)
    growth = forms.IntegerField(label='growth')
    creator_castle = forms.CharField(label='creator_castle', max_length=40)
