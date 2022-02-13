from django.contrib.auth.models import User
from django.forms import ModelForm, NumberInput

from django.forms import inlineformset_factory

from django import forms

from site_app.models import ClientRenter, SearchTable


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email'




SearchFormSet = inlineformset_factory(ClientRenter, SearchTable, fields=('date_work', 'location',
                                                                         'estimated_working_time',
                                                                         'text',
                                                                         'work_type'
                                                                         ), extra=1)

