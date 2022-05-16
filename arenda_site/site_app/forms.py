from django.contrib.auth.models import User
from django.forms import ModelForm, NumberInput, modelformset_factory
from django.forms import formset_factory
from django.forms import inlineformset_factory

from django import forms

from site_app.models import ClientRenter, SearchTable, ScopeWork, TypeService, Picture, Renter, Vehicle, \
    AdditionalEquipment, PhoneRenter


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email'


SearchFormSet = inlineformset_factory(ClientRenter, SearchTable, fields=('date_start_period_work',
                                                                         'date_end_period_work',
                                                                         'location',
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
                                            extra=1)

ImageFormSet = inlineformset_factory(Renter, Picture,
                                     fields=('img_ads',), extra=1, can_delete=False)

VehicleFormSet = inlineformset_factory(Renter, Vehicle, fields=('name_brand', 'weight', 'max_digging_depth_first', 'vehicle_height'),
                                     extra=1, can_delete=False)

PhoneFormSet = inlineformset_factory(Renter, PhoneRenter, fields=('phone',),
                                     extra=1, can_delete=False)

AdditionalFormSet = inlineformset_factory(Vehicle, AdditionalEquipment, fields=('description', 'params'),
                                     extra=1, can_delete=False)

