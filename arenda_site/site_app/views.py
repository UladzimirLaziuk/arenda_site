import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from site_app import models

# Create your views here.
from site_app.forms import SearchFormSet, formset_type_service, ImageFormSet
from site_app.models import ClientRenter, TypeService, ScopeWork


class RenterViewList(ListView):
    model = models.Renter
    template_name = 'main/list_renter.html'


class RenterViewCreate(CreateView):
    model = models.Renter
    template_name = 'main/create_renter.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        kwargs.update({'formset_img': ImageFormSet()})
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_img = ImageFormSet(self.request.POST, self.request.FILES)
        if form.is_valid() and formset_img.is_valid():
            return self.form_valid(form, formset_img)
        else:
            return self.form_invalid(form, formset_img)

    def form_invalid(self, form, formset_img):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  formset=formset_img))

    def form_valid(self, form, formset_img):
        obj_renter = form.save()
        # obj_query = self.set_objects_queryset()
        # obj_query.update(**form.cleaned_data)
        formsets = formset_img.save(commit=False)
        for frs in formsets:
            frs.ad_link = obj_renter
            frs.save()
        return redirect(reverse("renter_list"))


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

            for form in formset_search:
                obj_table = form.save(commit=False)
                obj_table.client_renter = obj
                obj_table.save()

            for element in form_set_type:
                obj = element.save(commit=False)
                obj.type_work = element.cleaned_data['type_work']
                obj.scope_of_work = element.cleaned_data['scope_of_work']
                obj.scope_work_and_type = obj_table
                obj.save()
                print(type(obj))

        return HttpResponse()


class RenterUpdateView(UpdateView):
    model = models.Renter
    fields = '__all__'
    template_name = 'main/update_renter.html'
    success_url = "/"

    def get_context_data(self, **kwargs):
        kwargs.update({'formset_img': ImageFormSet()})  # initial
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_img = ImageFormSet(self.request.POST, request.FILES)
        if form.is_valid() and formset_img.is_valid():
            return self.form_valid(form, formset_img)
        else:
            return self.form_invalid(form, formset_img)

    def form_invalid(self, form, formset_img):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  formset=formset_img))

    def form_valid(self, form, formset_img):
        obj_renter = form.save(commit=False)
        obj_renter.save()
        form.save_m2m()

        formsets = formset_img.save(commit=False)
        for frs in formsets:
            frs.ad_link = obj_renter
            frs.save()
        return redirect(reverse("renter_list"))


class RenterDeleteView(DeleteView):
    model = models.Renter
    template_name = 'main/renter_confirm_delete.html'
    success_url = "/"


class RenterDetailView(DetailView):
    model = models.Renter
    fields = '__all__'
    template_name = 'main/detail_renter.html'
    success_url = "/"
