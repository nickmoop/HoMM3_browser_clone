from django import forms


class Login(forms.Form):
    user_name = forms.CharField(label='user_name', max_length=40)
    password = forms.CharField(label='password', max_length=40)


class Registration(forms.Form):
    user_name = forms.CharField(label='user_name', max_length=40)
    email = forms.CharField(label='email', max_length=40)
    password = forms.CharField(label='password', max_length=40)


class MakeSpell(forms.Form):
    name = forms.CharField(label='name', max_length=255)
    effect = forms.CharField(label='effect', max_length=255)
    radius = forms.IntegerField(label='radius')
    school = forms.CharField(label='school', max_length=255)
    formula = forms.CharField(label='formula', max_length=255)
    level = forms.IntegerField(label='level')
    description = forms.CharField(label='description', max_length=255)
    cost = forms.IntegerField(label='cost')


class MakeUnit(forms.Form):
    castle = forms.CharField(label='castle', max_length=40)
    name = forms.CharField(label='name', max_length=40)
    attack_skill = forms.IntegerField(label='attack_skill')
    defense_skill = forms.IntegerField(label='defense_skill')
    minimum_damage = forms.IntegerField(label='minimum_damage')
    maximum_damage = forms.IntegerField(label='maximum_damage')
    health = forms.IntegerField(label='health')
    speed = forms.IntegerField(label='speed')
    growth = forms.IntegerField(label='growth')
    special = forms.CharField(label='special', max_length=40)


class MakeBattle(forms.Form):
    name = forms.CharField(label='name', max_length=40)
    growth = forms.IntegerField(label='growth')
    creator_castle = forms.CharField(label='creator_castle', max_length=40)
