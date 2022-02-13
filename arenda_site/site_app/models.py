import calendar
import datetime
import logging

from django.db import models
# from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from site_app.bot_telegram import send_message

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Renter(models.Model):
    name_organization = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)  # ArrayField
    location = models.CharField(max_length=255)  # modul
    # types_of_services = ArrayField(models.CharField(max_length=255, blank=True), default=list)
    types_of_services = models.ManyToManyField('TypeService', blank=True)  # OR Arrayfield
    delivery = models.PositiveIntegerField(null=True, default=0)
    price_per_hour = models.PositiveIntegerField()
    # types_of_buckets = models.ForeignKey('Buckets', on_delete=models.SET_NULL, blank=True, null=True)
    # other_types_of_communication = models.ManyToManyField('Communication', blank=True)  # ??Choises
    # type_of_tractor = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f'{self.name_organization}'


class TypeService(models.Model):
    typework = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.typework}'


class ScopeWork(models.Model):
    scope_of_work = models.CharField(max_length=100)
    type_work = models.ForeignKey("TypeService", on_delete=models.CASCADE)
    scope_work_and_type = models.ForeignKey('SearchTable', on_delete=models.CASCADE, blank=True, null=True)


class Buckets(models.Model):
    renter_obj = models.ForeignKey('Renter', on_delete=models.CASCADE, blank=True, null=True, related_name='buckets')
    size_bucket = models.CharField(max_length=20)


class Communication(models.Model):
    other_types_of_communication = models.ForeignKey('Renter', on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)


class AdditionalEquipment(models.Model):
    equipment = models.ForeignKey('Renter', on_delete=models.CASCADE)
    type_equipment = models.CharField(max_length=1)


class Vehicle(models.Model):
    name_brand = models.CharField(max_length=255)
    additional_equipment = models.ForeignKey('AdditionalEquipment', on_delete=models.SET_NULL, blank=True,
                                             null=True)  # Arrayfield
    renter = models.ForeignKey('Renter', on_delete=models.CASCADE)
    weight = models.CharField(max_length=50)
    max_digging_depth = models.CharField(max_length=50)  # string or float
    vehicle_height = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name_brand}'


class BotDb(models.Model):
    group_id_bot = models.CharField(max_length=25, unique=True)


# class WorkType(models.Model):
#     work_type = models.ForeignKey('TypeService', on_delete=models.CASCADE)
#     lookup_table = models.ForeignKey('SearchTable', on_delete=models.CASCADE)


class SearchTable(models.Model):
    client_renter = models.ForeignKey('ClientRenter', on_delete=models.CASCADE)
    date_work = models.DateTimeField(default=timezone.now)  # period must
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


@receiver(post_save, sender=SearchTable)
def subscribe_message(sender, instance, **kwargs):
    logger.info("Instance {}".format(instance))
    send_message(BotDb.objects.all())
