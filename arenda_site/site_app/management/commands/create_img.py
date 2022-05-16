import json
import re
import os
import shutil
from django.core.files import File
import requests
from django.core.management import BaseCommand

from arenda_site.settings import MEDIA_ROOT
from site_app.models import RenterAd, Renter, Vehicle, Buckets, AdditionalEquipment, PhoneAd, PictureAdRenter

def get_name_photo(url):
    basename_path = url.split('?')[0]
    return os.path.basename(basename_path)


def re_write_img(pic=None):
    path_work_img = os.path.join(MEDIA_ROOT, 'image')

    path_dir_file = os.path.join(path_work_img, 'image_date')
    for pic in PictureAdRenter.objects.all():

        if pic.img_url and not pic.img_ads:

            # result = request.urlretrieve(self.img_url)
            # print(get_name_photo(self.img_url))
            file_name = get_name_photo(pic.img_url)

            path_for_file = os.path.join(path_dir_file, file_name)

            try:
                if os.path.isfile(path_for_file):
                    # print(pic.img_url)
                    print(path_for_file, file_name)
                    pic.img_ads.save(
                        file_name,
                        File(open(path_for_file, 'rb'))
                    )
                    pic.save()

            except FileNotFoundError as fileerror:
                print(fileerror.args)

def parse_photo_ad():
    pic_base = PictureAdRenter.objects.values_list('img_url', flat=True)
    path_work_img = os.path.join(MEDIA_ROOT, 'image')
    os.mkdir(os.path.join(path_work_img, 'image_date'))
    for img_url in pic_base:
        res = requests.get(img_url, stream=True)
        name_photo = get_name_photo(img_url)
        file_full_path = os.path.join(path_work_img, 'image_date', name_photo)
        if res.status_code == 200:

            with open(file_full_path, 'wb') as f:
                shutil.copyfileobj(res.raw, f)
            print('Image sucessfully Downloaded: ', file_full_path)
        else:
            print('Image Couldn\'t be retrieved')



class Command(BaseCommand):
    help = 'Create img'

    def handle(self, *args, **options):
        list_img_url = PictureAdRenter.objects.values_list('img_url', flat=True)
        set_img_name = {get_name_photo(img) for img in list_img_url}
        # print(set_img_name)
        path_work_img = os.path.join(MEDIA_ROOT, 'image', 'image_date')
        set_img_dir = set(os.listdir(path_work_img))
        path_work_for_img = os.path.join(MEDIA_ROOT, 'image')
        if not os.path.exists(path_work_for_img) or not os.listdir(path_work_for_img):
            parse_photo_ad()

        if set_img_dir.issubset(set_img_name):
            re_write_img()
            return
