from django.contrib import admin

# Register your models here.
from site_app.models import Renter, Vehicle

admin.site.register(Renter)
admin.site.register(Vehicle)