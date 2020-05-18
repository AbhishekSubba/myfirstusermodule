from django.db import models
import jsonfield
# Create your models here.


class tblUser(models.Model):
    Name = models.CharField(max_length=100)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)


class tblAccess_token(models.Model):
    username = models.CharField(max_length=30)
    Code = models.CharField(max_length=300)
    access_token = models.CharField(max_length=400)
    githublogin = models.CharField(max_length=200, null=True, blank=True)
    githubfullname = models.CharField(max_length=200, null=True, blank=True)
    emailid = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    Company = models.CharField(max_length=200, null=True, blank=True)


class tblWebhooks(models.Model):
    webhooks = jsonfield.JSONField()
