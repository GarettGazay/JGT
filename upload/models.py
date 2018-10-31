from django.db import models
from django.forms import ModelForm
from django.utils import timezone

class UploadCsv(models.Model):
    csv = models.FileField(upload_to='dashride_csv')
    upload_date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.csv)

class ConvertedFile(models.Model):
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    upload_date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.name)

class UploadForm(ModelForm):
    class Meta:
        model = UploadCsv
        fields = ('csv',)
