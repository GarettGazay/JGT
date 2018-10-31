from django.contrib import admin
from .models import UploadCsv,ConvertedFile

admin.site.register(UploadCsv)
admin.site.register(ConvertedFile)
