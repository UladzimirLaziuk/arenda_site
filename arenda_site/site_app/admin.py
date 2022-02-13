from django.contrib import admin

# Register your models here.
from site_app.models import Renter, Vehicle, ClientRenter, SearchTable, AdditionalEquipment, Communication, Buckets, \
    TypeService, ScopeWork

admin.site.register(Renter)
admin.site.register(Vehicle)
admin.site.register(ClientRenter)
admin.site.register(SearchTable)
admin.site.register(AdditionalEquipment)
admin.site.register(Communication)
admin.site.register(Buckets)
admin.site.register(TypeService)
admin.site.register(ScopeWork)
