from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from UserModule.models import tblUser
import json
from django.core import serializers
# Create your views here.
def list_item(request):
    return render(request,'UserModule/login.html')

def Create_Users(request):
    
    if request.method == 'POST':
        name = request.POST['strFullName']
        username= request.POST['LoginID']
        password=request.POST['Password']
        data={}
        try:
            tbu = tblUser(
                Name=name,
                username=username,
                password=password
            )
            tbu.save()
            data['Status']='Success'
            data['Name']=tbu.Name
        except:
            data['Status']='Error'
            data['message']='smething went wrong with data base'
    return JsonResponse(json.dumps(data),content_type="application/json",safe=False)
