from django.urls import path
from . import views
urlpatterns=[
    path('login/',views.list_item),
    path('UserRegistration/',views.Create_Users),
    path('',views.list_item)
]