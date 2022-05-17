import calendar
import datetime
import logging
import os
import urllib

from django.db import models
# from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from .tasks import send_sms_task
from sorl.thumbnail import ImageField

from phonenumber_field.modelfields import PhoneNumberField

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Renter(models.Model):
    name_organization = models.CharField(max_length=255)
    # phone = models.CharField(max_length=255)  # ArrayField
    location = models.CharField(max_length=255)  # modul
    # types_of_services = ArrayField(models.CharField(max_length=255, blank=True), default=list)

    # delivery = models.PositiveIntegerField(null=True, default=0, blank=True)
    # price_per_hour = models.PositiveIntegerField()
    # types_of_buckets = models.ForeignKey('Buckets', on_delete=models.SET_NULL, blank=True, null=True)
    # other_types_of_communication = models.ManyToManyField('Communication', blank=True)  # ??Choises
    # type_of_tractor = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f'{self.name_organization}'

    def get_absolute_url(self):
        return reverse("renter_detail", kwargs={"pk": self.id})


class Balance(models.Model):
    object_balance = models.OneToOneField(Renter, on_delete=models.CASCADE, primary_key=True)
    balance = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=0)


class PhoneRenter(models.Model):
    rent_phone = models.ForeignKey(Renter, on_delete=models.CASCADE,
                                   verbose_name='Телефон')
    phone = models.CharField(max_length=255)


class RenterPicture(models.Model):
    object_ads = models.ForeignKey(Renter, on_delete=models.CASCADE,
                                   verbose_name='Объект объявления', related_name='renter_picture')
    img_url = models.ImageField(verbose_name='Фото объявления', default='')

    class Meta:
        verbose_name = "Фото объявления"
        verbose_name_plural = "Фото объявлений"


class TypeService(models.Model):
    typework = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.typework}'


class ScopeWork(models.Model):
    scope_of_work = models.CharField(max_length=100)
    type_work = models.ForeignKey("TypeService", on_delete=models.CASCADE)
    scope_work_and_type = models.ForeignKey('SearchTable', on_delete=models.CASCADE, blank=True, null=True)


class Communication(models.Model):
    other_types_of_communication = models.ForeignKey('Renter', on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)


class Vehicle(models.Model):

    name_brand = models.CharField(max_length=255, blank=True)
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE)
    # weight = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, default=0)
    weight = models.FloatField(null=True, blank=True, default=None)
    weight_units = models.CharField(max_length=50, blank=True, null=True)

    max_digging_depth_first = models.FloatField(null=True, blank=True, default=0.0)
    max_digging_depth_second = models.FloatField(null=True, blank=True, default=0.0)
    # max_digging_depth = models.CharField(max_length=50, blank=True, null=True)  # string or float
    vehicle_height = models.FloatField(null=True, blank=True, default=0.0)

    def __str__(self):
        return f'{self.name_brand}'


class AdditionalEquipment(models.Model):
    description = models.CharField(max_length=100)
    vehicle_equipment = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    params = models.PositiveIntegerField(verbose_name='Параметр оборудования', blank=True, null=True)


class Buckets(models.Model):
    description = models.CharField(max_length=100, default='Ковш')
    vehicle_object = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    width = models.PositiveIntegerField(verbose_name='Ширина ковша')


class BotDb(models.Model):
    group_id_bot = models.CharField(max_length=25, unique=True)


# class WorkType(models.Model):
#     work_type = models.ForeignKey('TypeService', on_delete=models.CASCADE)
#     lookup_table = models.ForeignKey('SearchTable', on_delete=models.CASCADE)
def one_day_hence():
    return timezone.now() + timezone.timedelta(days=1)


class SearchTable(models.Model):
    client_renter = models.ForeignKey('ClientRenter', on_delete=models.CASCADE)
    date_start_period_work = models.DateTimeField(default=timezone.now)  # period must
    date_end_period_work = models.DateTimeField(default=one_day_hence)
    location = models.CharField(max_length=100)
    estimated_working_time = models.TimeField(verbose_name="Прeдполагаемое время работ", blank=True, null=True)
    text = models.CharField(max_length=255, verbose_name='Произвольный текст для видом и объемов работ', blank=True)
    date_search = models.DateTimeField(auto_now_add=True)
    # scope_work_and_type = models.ForeignKey('ScopeWork', on_delete=models.CASCADE, blank=True, null=True)


class ClientRenter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=100)

    # class Meta:
    #     models = AbstractUser
    #     field = ['email', 'first_name']


class Picture(models.Model):
    ad_link = models.ForeignKey(Renter, on_delete=models.CASCADE)
    img_ads = ImageField(upload_to='image/', default="image/pingvin_Shkiper.jpg")


class MessageId(models.Model):
    message_id = models.CharField(max_length=20)
    search_table_id = models.CharField(max_length=20)
    date_delete = models.CharField(max_length=20)


class RenterAd(models.Model):
    title = models.CharField(max_length=255)
    renter_ad = models.ForeignKey(Renter, on_delete=models.CASCADE)
    vehicle_ad = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    description = models.TextField()
    price_per_hour_from_float = models.FloatField(null=True, blank=True, default=None)
    price_per_hour_to_float = models.FloatField(null=True, blank=True, default=None)

    price_per_hour_from = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    price_per_hour_to = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)

    price_per_shift_from = models.FloatField(null=True, blank=True, default=None)
    price_per_shift_to = models.FloatField(null=True, blank=True, default=None)

    min_work_time = models.PositiveIntegerField(blank=True, null=True, default=0)
    work_weekends_time = models.CharField(max_length=255, blank=True, null=True)
    work_time = models.CharField(max_length=255, blank=True, null=True)
    place_work = models.CharField(max_length=255, blank=True, null=True)
    region_work = models.CharField(max_length=255, blank=True, null=True)
    delivery = models.CharField(max_length=255, blank=True, null=True)
    date_publication = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Дата публикации')
    types_of_services = models.ManyToManyField('TypeService', blank=True)

    def get_absolute_url(self):
        return reverse('renterad_detail', args=[str(self.pk)])


def get_name_photo(url):
    basename_path = url.split('?')[0]
    return os.path.basename(basename_path)


class PhoneAd(models.Model):
    ad_renter = models.ForeignKey(RenterAd, on_delete=models.CASCADE)
    phone_ad_renter = PhoneNumberField()


class PictureAdRenter(models.Model):
    ad_link = models.ForeignKey(RenterAd, on_delete=models.CASCADE)
    img_url = models.URLField(verbose_name='Фото url объявления', default='')
    smile_img_url = models.URLField(verbose_name='Фото smile url объявления', blank=True, null=True)
    img_ads = ImageField(upload_to='image/', default="")


@receiver(post_save, sender=SearchTable)
def subscribe_message(sender, instance, **kwargs):
    logger.info("Instance.id {}".format(instance.id))
    logger.info("kwargs {}".format(kwargs))
    send_sms_task.delay(instance.id)
    logger.info("Instance {}".format(instance))
