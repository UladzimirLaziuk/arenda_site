import os
import django
from django.utils.timezone import now
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arenda_site.settings')
django.setup()

from site_app.models import *


def create_vechicle_model(weight=2500, max_digging_depth=2400, vehicle_height=3800, name_brand='JCB 8027'):
    vehicle_model, create = Vehicle.objects.get_or_create(weight=weight,
                                                          max_digging_depth=max_digging_depth,
                                                          vehicle_height=vehicle_height,
                                                          name_brand=name_brand)

    return vehicle_model


def renter_model_create(name_brand=None):
    dict_renter = {
        'name_organization': 'Пробный И.П.',
        'phone': '+375291614741',
        'location': "Минск",
        'price_per_hour': 45,
        'type_of_tractor': create_vechicle_model(name_brand=name_brand)
    }
    renter, create = Renter.objects.get_or_create(**dict_renter)
    return renter


def create_type_work(path_file='type_work'):
    with open(path_file, 'r', encoding='utf-8') as ff_t:
        for el in ff_t:
            try:
                print(el)
                TypeService.objects.get_or_create(typework=el.strip())
            except Exception:
                print('Oops')
                break


create_type_work()

def func_probe(date_d=None):
    list_data = []
    for el in MessageId.objects.all():
        print(datetime.datetime.now())
        search_list = SearchTable.objects.filter(date_end_period_work__lte=now()).values_list('id', flat=True)



    return list_data




# renter_model_create(name_brand='JCB 8027')
# renter_model_create(name_brand='Wacker Neuson')


# cl_phil = ClientRenter.objects.get(pk=1)
# search = SearchTable.objects.create(client_renter=cl_phil, location='Minsk')
# print(search)

# type_s = TypeService.objects.create(typework='uborka', scope_of_work='20')
#
# ty = TypeService.objects.first()
# type_servise = TypeService.objects.all()
# user = User.objects.get(username='Probe')
# print(user)
# cli = ClientRenter.objects.get(user=user)
# print(cli)
# search_table, _ = SearchTable.objects.get_or_create(client_renter=cli,
#                                           location='Minsk', text='Bla-Bla')
#
#
# search_table.work_type.add(None)
#
#
# search = SearchTable.objects.first()
# print(search.work_type.all())