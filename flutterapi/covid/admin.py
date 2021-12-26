from django.contrib import admin

#from webapi.flutterapi.covid.serializers import heatmapSerializers
from .models import *

admin.site.register(imgProcess)
admin.site.register(heatmapModel)
# Register your models here.
