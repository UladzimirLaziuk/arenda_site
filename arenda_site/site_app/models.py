from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Renter(models.Model):
    name_organization = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)  # ArrayField
    location = models.CharField(max_length=255)  # modul
    # types_of_services = ArrayField(models.CharField(max_length=255, blank=True), default=list) TODO ILIA HELP
    types_of_services = models.ManyToManyField('TypeService', blank=True)  # OR Arrayfield
    delivery = models.PositiveIntegerField(null=True, default=0)
    price_per_hour = models.PositiveIntegerField()
    types_of_buckets = models.ForeignKey('Buckets', on_delete=models.SET_NULL, blank=True, null=True)
    other_types_of_communication = models.ManyToManyField('Communication', blank=True)  # ??Choises
    type_of_tractor = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    email = models.EmailField(blank=True)


class TypeService(models.Model):
    typework = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.typework}'


class Buckets(models.Model):
    pass


class Communication(models.Model):
    pass


class AdditionalEquipment(models.Model):
    pass


class Vehicle(models.Model):
    name_brand = models.CharField(max_length=255)
    additional_equipment = models.ForeignKey('AdditionalEquipment', on_delete=models.SET_NULL, blank=True,
                                             null=True)  # Arrayfield
    weight = models.PositiveIntegerField()
    max_digging_depth = models.PositiveIntegerField()  # string or float
    vehicle_height = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name_brand}'
