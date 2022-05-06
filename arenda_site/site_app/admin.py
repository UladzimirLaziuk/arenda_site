from django.contrib import admin

# Register your models here.
from site_app.models import Renter, Vehicle, ClientRenter, SearchTable, AdditionalEquipment, Communication, Buckets, \
    TypeService, ScopeWork, RenterPicture, PhoneRenter


class RenterPictureAdmin(admin.StackedInline):
    model = RenterPicture
    extra = 0


class VehicleAdmin(admin.StackedInline):
    model = Vehicle
    extra = 0

class PhoneAdmin(admin.StackedInline):
    model = PhoneRenter
    extra = 0

# class AdditionalEquipmentAdmin(admin.StackedInline):
#     model = AdditionalEquipment
#     extra = 0


class RenterAdmin(admin.ModelAdmin):
    inlines = [RenterPictureAdmin, VehicleAdmin, PhoneAdmin]


admin.site.register(Renter, RenterAdmin)

admin.site.register(ClientRenter)
admin.site.register(SearchTable)
admin.site.register(AdditionalEquipment)
admin.site.register(Communication)
admin.site.register(Buckets)
admin.site.register(TypeService)
admin.site.register(ScopeWork)
