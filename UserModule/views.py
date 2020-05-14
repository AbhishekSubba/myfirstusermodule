from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from UserModule.models import tblUser
import json
from django.core import serializers
# Create your views here.


def list_item(request):
    return render(request, 'UserModule/login.html')


def Create_Users(request):

    if request.method == 'POST':
        name = request.POST['strFullName']
        username = request.POST['LoginID']
        password = request.POST['Password']
        data = {}
        try:
            tbu = tblUser(
                Name=name,
                username=username,
                password=password
            )
            tbu.save()
            data['Status'] = 'Success'
            data['Name'] = tbu.Name
        except:
            data['Status'] = 'Error'
            data['message'] = 'smething went wrong with data base'
    return JsonResponse(json.dumps(data), content_type="application/json", safe=False)


def LoginValidate(request):
    if request.method == 'POST':
        LoginID = request.POST['LoginID']
        Password = request.POST['Password']
        data = {
            # 'message': serializers.serialize('json', tblUser.objects.filter(username=LoginID))
        }
        try:
            tbu = serializers.serialize(
                'json', tblUser.objects.filter(username=LoginID))
            if len(tbu) > 0:
                data['Status'] = 'Success'
                parsed_json = (json.loads(tbu))
                dataJsn = json.dumps(parsed_json, indent=4, sort_keys=True)
                loaded_json = json.loads(dataJsn)
                if loaded_json[0]["fields"]["password"] == Password:
                    data['message'] = loaded_json[0]["fields"]["Name"]
                else:
                    data['Status'] = 'Error'
                    data['message'] = "Invalid password"
        except:
            data['Status'] = 'Error'
            data['message'] = 'smething went wrong with data base'
    return JsonResponse(data, content_type="application/json", safe=False)


def admin(request):
    return render(request, 'UserModule/admin.html')
