from django.db import models
from account.models import Users
# Create your models here.

class pets(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed=models.CharField()
    gender=models.CharField()
    price=models.FloatField()
    image=models.ImageField(upload_to='pets/')
    quantity=models.IntegerField(default=1)


class Cart(models.Model):
    user=models.ForeignKey(Users,on_delete=models.CASCADE)    
    pet=models.ForeignKey(pets,on_delete=models.CASCADE)   
    quantity=models.IntegerField(default=0)
    total_price=models.IntegerField(default=0)
    grand_total=models.IntegerField(default=0)

class Payments(models.Model):
    user=models.ForeignKey(Users,on_delete=models.CASCADE)
    pet=models.ForeignKey(Cart,on_delete=models.CASCADE)
    amount=models.FloatField()
    payment_id=models.CharField()
    razorpay_payment_id=models.CharField()
    razorpay_order_id=models.CharField()
    razorpay_signature=models.CharField()

class Delivery_details(models.Model):
    user=models.ForeignKey(Users,on_delete=models.CASCADE)
    pet=models.ForeignKey(Cart,on_delete=models.CASCADE)
    amount=models.FloatField()
    user_token=models.IntegerField()
    delivery_token=models.IntegerField()
    address=models.CharField()
    delivery_status=models.CharField(max_length=20, default='pending')


