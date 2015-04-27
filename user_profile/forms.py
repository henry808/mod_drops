
from django import forms
from django.forms import Form
from django.forms.models import inlineformset_factory
from user_profile.models import UserProfile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone',
                  'picture',
                  'birthday',
                  'name_privacy',
                  'phone_privacy',
                  'email_privacy',
                  'pic_privacy',
                  'birthday_privacy']


    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.CharField()