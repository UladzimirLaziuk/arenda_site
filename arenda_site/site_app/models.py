from django.db import models


# Create your models here.
class Renter(models.Model):
    name_organization = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)  # ArrayField
    location = models.CharField(max_length=255)  # modul
    types_of_services = models.ManyToManyField('TypeService', on_delete=models.CASCADE)  # OR Arrayfield
    delivery = models.PositiveIntegerField(null=True, default=0)
    price_per_hour = models.PositiveIntegerField()
    types_of_buckets = models.ForeignKey('Buckets', on_delete=models.CASCADE)
    other_types_of_communication = models.ManyToManyField('Communication', blank=True)  # ??Choises
    type_of_tractor = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    email = models.EmailField(blank=True)


class TypeService(models.Model):
    pass


class Buckets(models.Model):
    pass


class Communication(models.Model):
    pass


class AdditionalEquipment(models.Model):
    pass


class Vehicle(models.Model):
    additional_equipment = models.ForeignKey('AdditionalEquipment', on_delete=models.CASCADE, blank=True)  # Arrayfield
    weight = models.PositiveIntegerField(blank=True)
    max_digging_depth = models.PositiveIntegerField(blank=True)
    vehicle_height = models.PositiveIntegerField(blank=True)
