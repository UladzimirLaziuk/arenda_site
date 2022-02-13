import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from site_app import models

# Create your views here.
from site_app.forms import SearchFormSet, formset_type_service
from site_app.models import ClientRenter, TypeService, ScopeWork


class RenterViewList(ListView):
    model = models.Renter
    template_name = 'main/list_renter.html'


class RenterViewCreate(CreateView):
    model = models.Renter
    template_name = 'main/create_renter.html'
    fields = '__all__'


##TODO Permission
class RenterViewSearch(CreateView):
    model = models.ClientRenter
    template_name = 'main/search_renter.html'
    fields = ('phone',)

    def get_context_data(self, **kwargs):
        kwargs.update({'formset_search': SearchFormSet()})
        kwargs.update({'formset_type_service': formset_type_service(queryset=ScopeWork.objects.none())})
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):

        #
        form_class = self.get_form_class()
        form_renter = form_class(request.POST)
        form_set_type = formset_type_service(data=request.POST)
        # form = form_class(request.POST)
        # user_renter, _ = ClientRenter.objects.get_or_create(user=self.request.user)
        formset_search = SearchFormSet(request.POST)

        if form_renter.is_valid() and formset_search.is_valid() and form_set_type.is_valid():
            obj = form_renter.save(commit=False)
            obj.user = self.request.user
            obj.save()
            print(obj)

            for form in formset_search:
                obj_table = form.save(commit=False)
                obj_table.client_renter = obj
                obj_table.save()
            print('==================================', obj_table)
            for element in form_set_type:
                obj = element.save(commit=False)
                obj.type_work = element.cleaned_data['type_work']
                obj.scope_of_work = element.cleaned_data['scope_of_work']
                obj.scope_work_and_type = obj_table
                obj.save()
                print(type(obj))

                # obj_c.scope_work_and_type = obj

        #
        #
        #

        return HttpResponse()
    #             print('====================================================')
    #             obj = formset_search.save(commit=False)
    #             for form in obj:
    #                 form.client_renter = user_renter
    #
    #
    #
    #
    #             # obj = formset_worktype.save()
    #
    #             print(TypeService.objects.count())
    #             # print(obj_new, '--------------')
    #             # form.work_type.add(obj)
    #             print(TypeService.objects.count())
    #
    #
    #
    #
    #             print(form, "++++++++++++++++++++++++++++++++++++++++++++")
    #             # print(obj.save())
    #             # print(formset_search)
    #             # print(formset_worktype)
    #             return HttpResponse()
    #         else:
    #             print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    #     except ValueError:
    #         print('------------------------------------------------------------------------------')
    #         return
