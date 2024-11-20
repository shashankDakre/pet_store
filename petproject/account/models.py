from django.db import models

class Users(models.Model):
    name=models.CharField()
    email=models.EmailField(unique=True)
    mobile=models.BigIntegerField(unique=True)
    city=models.CharField()
    state=models.CharField()
    address=models.CharField()
    password=models.CharField()

class Profile_pic(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE) 
    profile_pic = models.ImageField(upload_to='profile/')