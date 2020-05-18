from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from UserModule.models import *
import json
from django.core import serializers
import requests
from django.views.decorators.csrf import csrf_exempt
from decouple import config
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
        request.session['UserLoginid'] = LoginID
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
    username = request.session.get('UserLoginid')
    return render(request, 'UserModule/admin.html', {'username': username, 'client_id': config('client_id')})


def GenerateAccesstoken(request):
    if request.method == 'GET':
        code = request.GET['code']
        client_id = config('client_id')
        client_secret = config('client_secret')
        # redirect_uri = "http://127.0.0.1:8000/UserModule/callback/"
        redirect_uri = "https://myfirstusermodule.herokuapp.com/UserModule/callback/"
        token_url = "https://github.com/login/oauth/access_token?client_id=" + client_id + \
            "&redirect_uri=" + redirect_uri + "&client_secret=" + \
            client_secret + "&code=" + code
        headers = {"content-type": "application/x-www-form-urlencoded",
                   "Accept": "application/json"}
        response = requests.post(token_url, headers=headers)
        requet_token = response.content.decode()
        requet_tokenJson = json.loads(requet_token)
        access_token = requet_tokenJson["access_token"]
        GetGithubUserDetails(request, code, access_token)
        username = request.session.get('UserLoginid')
    return render(request, 'UserModule/GithubAuthSuccess.html', {'username': username})


def GetGithubUserDetails(request, code, access_token):
    urlForUser = "https://api.github.com/user?access_token=" + access_token
    headers = {"content-type": "application/x-www-form-urlencoded",
               "Accept": "application/json"}
    response = requests.get(urlForUser, headers=headers)
    userDetails = json.loads(response.content.decode())
    act = tblAccess_token(
        username=request.session.get('UserLoginid'),
        Code=code,
        access_token=access_token,
        githublogin=userDetails["login"],
        githubfullname=userDetails["name"],
        emailid=userDetails["email"],
        location=userDetails["location"],
        Company=userDetails["company"]
    )
    act.save()


def findlogs(request):
    return render(request, 'UserModule/logs.html')


def getLogsForWebhooks(request):
    if request.method == 'POST':
        ID = request.POST['ID']
        username = request.session.get('UserLoginid')
        validUser = False
        if username == "abhi":
            validUser = True
        if ID == "1":
            data = tblAccess_token.objects.all()
            datajsn = serializers.serialize('json', data)
            datajsn = json.loads(datajsn)
            for d in datajsn:
                del d['pk']
                del d['model']
            parsed_json = json.dumps(datajsn, indent=4, sort_keys=True)
            parsed_json = json.loads(parsed_json)
            parsed_jsonobj = {}
            length = len(parsed_json)
            for i in range(0, length):
                parsed_jsonobj[i] = parsed_json[i]["fields"]
            finaldata = {'length': length,
                         'data': parsed_jsonobj, 'Success': validUser}
            return JsonResponse(finaldata, content_type="application/json", safe=False)
        else:
            data = tblWebhooks.objects.all()
            datajsn = serializers.serialize('json', data)
            datajsn = json.loads(datajsn)
            for d in datajsn:
                del d['pk']
                del d['model']
            parsed_json = json.dumps(datajsn, indent=4, sort_keys=True)
            parsed_json = json.loads(parsed_json)
            parsed_jsonobj = {}
            length = len(parsed_json)
            for i in range(0, length):
                parsed_jsonobj[i] = parsed_json[i]["fields"]
            finaldata = {'length': length,
                         'data': parsed_jsonobj, 'Success': validUser}
            return JsonResponse(finaldata, content_type="application/json", safe=False)


@csrf_exempt
def getPayload(request):
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            jsondata = request.body
            parsed_json = json.loads(jsondata)
            print(parsed_json)
            webhook = tblWebhooks(webhooks=parsed_json)
            webhook.save()
            return JsonResponse(parsed_json, content_type="application/json", safe=False)
