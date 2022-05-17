import json
import re

from django.core.management import BaseCommand

from site_app.models import RenterAd, Renter, Vehicle, Buckets, AdditionalEquipment, PhoneAd, PictureAdRenter
from django.core.management import call_command

def open_read_json(path):
    with open(path, 'r') as jsf:
        json_file = jsf.read()
        return json_file


def load_json(path):
    return json.loads(open_read_json(path))


def dict_map(dict_first, dict_second):
    result = {}
    for key, val in dict_first.items():
        result[val] = dict_second.get(key)
    return result

def zip_list_data(data):
    list_fields ='max_digging_depth_first', 'max_digging_depth_second'
    dict_result = {}
    for keys, value in zip(data, list_fields):
        dict_result[value] = keys
    return dict_result


def re_max_digging(data):
    pat = re.compile(r'(\d+.\d+|\d+)')
    return re.findall(pat, str(data))


def re_weight(data):
    pattern = re.compile(r'(\d+)')
    list_weight = re.findall(pattern, str(data))
    return list_weight[0]



def re_price_parser(data, pattern_name):
    dict_pattern = {
        "pattern_per_shift":re.compile(r'цена за смену:.\D*(\d+-\s\d+|\d+)'),
        "pattern_per_hour": re.compile(r'цена за час:.\D*(\d+\s*-\s*\d+|\d{1,2})')

    }
    pattern = dict_pattern.get(pattern_name)
    result = re.search(pattern, data)
    if result:
        data_result = result.group(1).split('-')
        dict_result = map(int, data_result)
        if len(data_result) < 2:

            data_result.append('0')
    else:
        data_result = ['0','0']
    return  data_result



class Command(BaseCommand):
    help = 'Create basel'

    def handle(self, *args, **options):
        path = 'renter.json'
        list_objects = load_json(path)['rental base']
        set_key = set()

        dict_json_or = {'min_work_time', 'phone_list', 'url_photo_smile', 'price', 'Ковш', 'title', 'data_url',
                        'url_org', 'desc', 'place_work', 'work_time', 'name_org', 'Макс. глубина копания',
                        'Навесное оборудование', 'Доставка', 'list_img', 'data_image', 'region_work', 'Масса',
                        'data_product', 'work_weekends_time'}

        dict_ad = {'title': 'title', "Доставка": "delivery", "desc": "description", "price": "price",
                   'work_time': "min_work_time", 'min_work_time': 'min_work_time', 'place_work': 'place_work',
                   'region_work': 'region_work',
                   'work_weekends_time': 'work_weekends_time',
                   }
        dict_rental = {"region_work": 'location', 'name_org': 'name_organization'}

        dict_vehicle = {
            "Масса": "weight",
            "Макс. глубина копания": "max_digging_depth",
        }


        for data_json in list_objects:

            try:
                result_rental_map = dict_map(dict_rental, data_json)

                result_vehicle_map = dict_map(dict_vehicle, data_json)
                digging_depth_list = result_vehicle_map.pop("max_digging_depth")
                if digging_depth_list:
                    result_re = re_max_digging(digging_depth_list)

                    if result_re:
                        dict_result = zip_list_data(result_re)
                        result_vehicle_map.update(**dict_result)



                rental_obj, _ = Renter.objects.get_or_create(**result_rental_map)

                result_ad_map = dict_map(dict_ad, data_json)
                data_price = result_ad_map.pop('price')
                data_hour = re_price_parser(data_price, "pattern_per_hour")
                data_per_shift = re_price_parser(data_price, "pattern_per_shift")

                result_ad_map.update({'price_per_hour_from': data_hour[0], 'price_per_hour_to': data_hour[1],
                                      'price_per_hour_from_float': data_hour[0], 'price_per_hour_to_float': data_hour[1],
                                      'price_per_shift_from': data_per_shift[0], 'price_per_shift_to': data_per_shift[1]
                                      })
                delivery = result_ad_map.pop('delivery', None)
                if delivery:
                    result_ad_map.update({'delivery':delivery[0]})

                result_vehicle_map.update({"renter": rental_obj})

                weight_list = result_vehicle_map.pop('weight', None)
                if weight_list:
                    weight = re_weight(weight_list)
                    result_vehicle_map.update({'weight': weight, 'weight_units': weight_list[-1]})

                vehicle_obj, _ = Vehicle.objects.get_or_create(**result_vehicle_map)

                result_ad_map.update({"renter_ad": rental_obj, "vehicle_ad": vehicle_obj})
                renter_ad_obj, _ = RenterAd.objects.get_or_create(**result_ad_map)
                data_buckets = data_json.get("Ковш")
                if data_buckets:
                    pattern = re.compile(r'(\d+)')
                    size_bucket_list = re.findall(pattern, str(data_buckets))
                    for width in size_bucket_list:
                        obj_buckets, _ = Buckets.objects.get_or_create(width=int(width), vehicle_object=vehicle_obj)
                data_additionalequipment_list = data_json.get("Навесное оборудование")
                if data_additionalequipment_list:
                    for description in data_additionalequipment_list:
                        obj_additionalequipment, _ = AdditionalEquipment.objects.get_or_create(description=description,
                                                                                               vehicle_equipment=vehicle_obj)
                phone_list = data_json.get("phone_list")
                for phone in phone_list:
                    phone_obj, _ = PhoneAd.objects.get_or_create(phone_ad_renter=phone, ad_renter=renter_ad_obj)

                img_list = data_json.get("list_img")
                if img_list:
                    for img_smile, img in img_list:
                        picture_ad_obj, _ = PictureAdRenter.objects.get_or_create(ad_link=renter_ad_obj, img_url=img,
                                                                                  smile_img_url=img_smile)
                else:
                    img_smile = data_json.get('url_photo_smile')
                    img = data_json.get('data_image')
                    picture_ad_obj, _ = PictureAdRenter.objects.get_or_create(ad_link=renter_ad_obj, img_url=img,
                                                                              smile_img_url=img_smile)

            except Exception as e:
                print('Oops')
                print(e.args)
                break
        else:
            call_command('create_img')
            call_command('create_model')
