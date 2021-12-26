from django.db import models
from django.db.models import fields
from rest_framework import serializers 
from .models import *

class covidSerializers(serializers.ModelSerializer):
    class Meta:
        model = imgProcess
        fields = ('id','img')
class heatmapSerializers(serializers.ModelSerializer):
    class Meta:
        model = heatmapModel
        fields = ('id','imgHeatmap')
