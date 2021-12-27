from django.shortcuts import render
from django.http import JsonResponse, response
import tensorflow as tf
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status 
from .serializers import covidSerializers, heatmapSerializers
from .models import heatmapModel, imgProcess
from .ml import *
import requests
last_conv_layer_name = "conv_pw_13_relu"
model  = tf.keras.models.load_model('/mobilenet.h5')
def runML(path):
    BS=8
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224,224))
    image_array = np.expand_dims(image, axis=0)
    image_array = np.array(image_array) / 255.0
    heatmap = make_gradcam_heatmap(image_array, model, last_conv_layer_name)
    cam_path = save_and_display_gradcam(image, heatmap)
    predict = model.predict(image_array, batch_size=BS)
    predict = np.argmax(predict, axis=1)
    return predict,cam_path
#get data
@api_view(['GET'])
def getData(request):
    allData = imgProcess.objects.all()
    serializers = covidSerializers(allData,many=True)
    return Response(serializers.data,status=status.HTTP_200_OK)
def getimg(request):
    data = heatmapModel.objects.name('test.png')
    serializers = heatmapSerializers(data,many=True)
    return Response(serializers.data,status=status.HTTP_200_OK)

@api_view(['POST'])
def postData(request):
    if request.method=='POST':
        serializers = covidSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            label,heatmap = runML(serializers.data['img'])
            if (label==0):
                predict = "Positive"
            else :
                predict = "Negative"
            heatmap = keras.preprocessing.image.img_to_array(heatmap)
            print(heatmap)
            path = 'heatmap/'
            cv2.imwrite(path+'test2.png',heatmap)
            HeatmapSerializers=heatmapSerializers(data={'imgHeatmap': cv2.imread(path+'test2.png') })
            if HeatmapSerializers.is_valid():
               HeatmapSerializers.save()
            else:
               print(HeatmapSerializers.errors)
            return Response(predict,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_404_NOT_FOUND)

data = [{'message':'HeloWorld',
            'subtitle':'เทสๆๆ',},{'message':'HeloWorld'}]


def Home(request):
    return JsonResponse(data=data,safe=False,json_dumps_params={'ensure_ascii' : False})

# Create your views here.
