from django.db import models

class imgProcess(models.Model):
    img = models.ImageField(upload_to = "images/")
class heatmapModel(models.Model):
    imgHeatmap = models.ImageField(upload_to = "heatmap/")
# Create your models here.
