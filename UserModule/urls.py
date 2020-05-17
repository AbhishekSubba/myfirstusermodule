from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.list_item),
    path('UserRegistration/', views.Create_Users),
    path('', views.list_item),
    path('UserLogin/', views.LoginValidate),
    path('GithubAuth/', views.admin),
    path('findlogs/', views.findlogs),
    path('callback/', views.GenerateAccesstoken),
    path('getLogs/', views.getLogsForWebhooks)
]
