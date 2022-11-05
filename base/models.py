from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=255,unique=True)
    bio = models.TextField()
    profile_img = models.CharField(max_length=255,blank=True,null=True)
    location = models.CharField(max_length=255,blank=True,null=True)
    url = models.CharField(max_length=255,blank=True,null=True, unique=True)

    def __str__(self):
        return self.name
class Advocate(models.Model):
    company =models.ForeignKey(Company,on_delete=models.SET_NULL, null =True, blank=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=200, unique=True)
    bio = models.TextField()
    profile_pic = models.CharField(max_length=255, blank=True,null=True)
    twitter = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
