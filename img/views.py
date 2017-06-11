from django.shortcuts import render
from django.http import HttpResponse
from img.models import img
from cloud import settings
# Create your views here.

def index(request):
    img_list =img.objects.all()
    images_list=[]
    for i in range(len(img_list) - 1, 0, -1):
        images_list.append(img_list[i])
    return render(request,'index.html',{'images':images_list})
