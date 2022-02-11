from django.db import models
# from django.contrib.postgres.fields import ArrayField


# Create your models here.
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
