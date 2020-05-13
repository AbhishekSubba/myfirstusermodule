from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from UserModule.models import tblUser
# Create your views here.
def list_item(request):
    return render(request,'UserModule/login.html')

def Create_Users(request):
    if request.method == 'POST':
        name = request.POST['strFullName']
        username= request.POST['LoginID']
        password=request.POST['Password']

        tbu = tblUser(
            Name=name,
            username=username,
            password=password
        )
        tbu.save()
        return JsonResponse('')