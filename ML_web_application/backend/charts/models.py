from django.db import models

class upload_model(models.Model):
    data_file = models.FileField()