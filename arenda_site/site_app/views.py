import logging

import requests
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from site_app import models
from rest_framework import status
# Create your views here.
from site_app.forms import SearchFormSet, formset_type_service, ImageFormSet, VehicleFormSet, PhoneFormSet, \
    AdditionalFormSet
from site_app.models import ClientRenter, TypeService, ScopeWork, RenterAd
from django.contrib.auth.mixins import LoginRequiredMixin

from site_app.serializers import MyRenterAdSerializer, RenterDetailViewSerializer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MyTemplateHTMLRenderer(TemplateHTMLRenderer):
    def get_template_context(self, object_list, renderer_context):
        response = renderer_context['response']
        if response.exception:
            object_list['status_code'] = response.status_code
        context = {'object_list': object_list}

        return context


DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10


class MyTemplateHTMLRendererDetail(TemplateHTMLRenderer):
    def get_template_context(self, object, renderer_context):
        response = renderer_context['response']
        if response.exception:
            object['status_code'] = response.status_code
        return {'object': object}


class CustomPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),

            },
            'total': self.page.paginator.count,
            'page': int(self.request.GET.get('page', DEFAULT_PAGE)),  # can not set default = self.page
            'page_size': int(self.request.GET.get('page_size', self.page_size)),
            'results': data
        })


class RenterAdViewList(ListAPIView):
    renderer_classes = [MyTemplateHTMLRenderer]
    pagination_class = CustomPagination
    serializer_class = MyRenterAdSerializer
    template_name = 'main/list_renter.html'
    queryset = models.RenterAd.objects.all().order_by('id')


class RenterViewCreate(CreateView):
    model = models.Renter
    template_name = 'main/create_renter.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        kwargs.update({'formset_img': ImageFormSet()})  # initial
        kwargs.update({'formset_vehicle': VehicleFormSet()})
        kwargs.update({'formset_phone': PhoneFormSet()})
        kwargs.update({'formset_additional': AdditionalFormSet()})
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        print(request.POST)
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
        return redirect(reverse("renter_ads_list"))


class RenterViewSearch(LoginRequiredMixin, CreateView):
    model = models.ClientRenter
    template_name = 'main/search_renter.html'
    fields = ('phone',)
    login_url = None

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
        kwargs.update({'formset_vehicle': VehicleFormSet()})
        kwargs.update({'formset_phone': PhoneFormSet()})
        kwargs.update({'formset_additional': AdditionalFormSet()})
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
        return redirect(reverse("renter_ads_list"))


class RenterDeleteView(DeleteView):
    model = models.Renter
    template_name = 'main/renter_confirm_delete.html'
    success_url = "/"


class RenterDetailView(DetailView):
    model = models.RenterAd
    fields = '__all__'
    template_name = 'main/detail_renter.html'
    # success_url = "/"


class RenterDetailView(RetrieveAPIView):
    renderer_classes = [MyTemplateHTMLRendererDetail]
    template_name = 'main/detail_renter.html'
    serializer_class = RenterDetailViewSerializer
    queryset = RenterAd.objects.all().order_by('id')


def filter_generator_create(request_data: dict, date_filter: str = ''):
    """returns a generator for filtering"""
    DICT_FILTER = {
        'price_per_hour_to': 'price_per_hour_from_float__lte',
        'price_per_hour_from': 'price_per_hour_from_float__gte',

        'price_per_shift_from': 'price_per_shift_from__gte',
        'price_per_shift_to': 'price_per_shift_to__lte',

        'date_from': 'date_publication__gte',
        'date_to': 'date_publication_lte',

        'min_work_time': 'min_work_time',
        'work_weekends_time': 'work_weekends_time',
        # 'work_time': 'work_time',
        'region_work': 'region_work',

        'delivery': 'delivery',

        'weight_from': 'vehicle_ad__weight__gte',
        'weight_to': 'vehicle_ad__weight__lte',

        'vehicle_height_to':'vehicle_ad__vehicle_height__lte',
        'vehicle_height_from': 'vehicle_ad__vehicle_height__gte',

        'max_digging_depth_to': 'vehicle_ad__max_digging_depth_first__lte',
        'max_digging_depth_from': 'vehicle_ad__max_digging_depth_first__gte',

        'types_of_services': 'types_of_services__in',
        'additionalequipment': 'vehicle_ad__additionalequipment__description__in',
        'buckets': 'vehicle_ad__buckets__width__in',
        'name_brand': 'vehicle_ad__name_brand__in',
        'renter': 'renter_ad__name_organization__in',
    }

    dict_data_request = {DICT_FILTER.get(key): val for key, val in request_data.items()
                         if val != date_filter and key in DICT_FILTER.keys()}

    return dict_data_request


def func_create_Q_list(dict_date, data_region_default=('г. Москва')):
    q = Q()
    for key, value in dict_date.items():

        # if key == 'date_publication__gte' or key == 'date_publication__lte':
        #     format = "%d.%m.%Y"
        #     value = datetime.datetime.strptime(value, format).date()
        q.children.append((key, value))
    return q


def func_sort_data(dt):
    DICT_MAP_SORT = {'По дате': 'date_ads',
                     'По дате-': '-date_ads',
                     'По цене': 'price_per_hour_from',
                     'По цене -': '-price_per_hour_from',
                     'По массе': 'vehicle_ad__weight',
                     'По массе-': '-vehicle_ad__weight',
                     'По глубине копания': 'vehicle_ad__max_digging_depth_first',
                     'По глубине копания-': '-vehicle_ad__max_digging_depth_first',
                     }

    sort_data = DICT_MAP_SORT.get(dt, 'id')
    return sort_data


class FilterSearchApiView(ListAPIView):
    # renderer_classes = [MyTemplateHTMLRenderer]
    pagination_class = CustomPagination
    serializer_class = MyRenterAdSerializer
    template_name = 'main/list_renter.html'
    queryset = models.RenterAd.objects.all().order_by('id')

    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        logger.info(f'Requests-{self.request.data}')
        sort_data = func_sort_data(self.request.data.get('sort'))
        # logger.info(f'Sort - {sort_data}')

        if self.request.data:
            result = filter_generator_create(request_data=self.request.data)
            # logging.info(f'Result-filter_generator_create --  {result}')
            filter_list = func_create_Q_list(result)
            queryset = RenterAd.objects.filter(filter_list).distinct().order_by(sort_data)

        else:
            queryset = RenterAd.objects.none

        return queryset

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    #
    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
