from django.contrib.auth.models import User
from django.forms import ModelForm, NumberInput, modelformset_factory
from django.forms import formset_factory
from django.forms import inlineformset_factory

from django import forms

from site_app.models import ClientRenter, SearchTable, ScopeWork, TypeService, Picture, Renter


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email'


SearchFormSet = inlineformset_factory(ClientRenter, SearchTable, fields=('date_work', 'location',
                                                                         'estimated_working_time',
                                                                         'text',
                                                                         ), extra=1, can_delete=False, )


class ScopeWorkForm(forms.ModelForm):
    class Meta:
        model = ScopeWork
        fields = 'scope_of_work', 'type_work'


def count_extra():
    return TypeService.objects.count()


formset_type_service = modelformset_factory(ScopeWork,

                                            fields=('type_work', 'scope_of_work'),
                                            extra=2)

ImageFormSet = inlineformset_factory(Renter, Picture,
                                     fields=('img_ads',), extra=1, can_delete=False)
