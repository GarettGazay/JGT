from django.contrib import admin
from .models import FormBasic, Reocurring, UniversalOneWay

admin.site.register(Reocurring)
admin.site.register(FormBasic)
admin.site.register(UniversalOneWay)
