from django.shortcuts import render,redirect
from pets.models import pets,Cart,Payments,Delivery_details
from django.contrib import messages
from account.models import Users,Profile_pic
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import razorpay
import random


def index(request):
    return render(request, 'index.html')

def profile(request):
    user = request.session.get('id')
    user = Users.objects.get(id =user)
    try:
      profile_pic = Profile_pic.objects.get(user=user)
      return render (request,"profile.html",{'user':user,'profile_pic':profile_pic})
    except Profile_pic.DoesNotExist:
      return render(request,"profile.html",{"reads":user})


    
def savetocart(request,id):
    user_id=request.session.get('id')
    user=Users.objects.get(id=user_id)
    pet=pets.objects.get(id=id)
    try:
        cart_check=Cart.objects.get(user=user,pet=pet)
        return redirect('/cart/')
    except ObjectDoesNotExist:
        cart=Cart.objects.create(user=user,pet=pet)
        cart.save()
        return redirect('/cart/')
    return render(request, 'profile.html')

def cart(request):
    user_id=request.session.get('id')
    user=Users.objects.get(id=user_id)
    carts=Cart.objects.filter(user=user)
    grand_total = sum(item.quantity * item.pet.price for item in carts)
    return render(request, 'cart.html',{'carts':carts,'grand_total':grand_total})

def checkout(request):
    return render(request, 'checkout.html')

def pay(request):
    return render(request, 'pay.html')

def orders(request):
    return render(request, 'orders.html')



def product(request):
    pts=pets.objects.all().order_by('id')
    if request.method=="POST":
        max_price=request.POST["max_price"]
        min_price=request.POST["min_price"]
        breed=request.POST["breed"]
        min_age=request.POST["min_age"]
        max_age=request.POST["max_age"]
        name=request.POST["name"]
        gender=request.POST["gender"]
        if name:
            pts = pets.objects.filter(name=name)
        if min_price:
            pts = pets.objects.filter(price__gte=min_price)
        if max_price:
            pts = pets.objects.filter(price__lte=max_price)
        if breed:
            pts = pets.objects.filter(breed=breed)
        if min_age:
            pts = pets.objects.filter(age__gte=min_age)
        if max_age:
            pts = pets.objects.filter(age__lte=max_age)
        if gender:
            pts = pets.objects.filter(gender=gender)
        return render(request,"product.html",{'pts':pts})    
    return render(request, 'product.html', {'pts':pts})

def wishlist(request):
    return render(request, 'wishlist.html')

def contact(request):
    return render(request, 'contact.html')

def pet(request):
    pts=pets.objects.all().order_by('id')
    return render(request, 'product.html', {'pts':pts})

def remove_cart(request,id):
    cart=Cart.objects.get(id=id)
    cart.delete()
    return redirect("/cart/")


def search(request):
    if request.method=="POST":
        search=request.POST['search']
        pts=pets.objects.filter(
            Q(name__icontains=search) |
            Q(breed__icontains=search) |
            Q(gender__icontains=search) |
            Q(age__icontains=search) 
    ) if search else []
        return render (request,'product.html',{'pts':pts})
    

def update_quantity(request,id,action):
    cart_item = Cart.objects.get(id=id)
    if action == "plus":
      cart_item.quantity += 1
      cart_item.total_price = cart_item.pet.price * cart_item.quantity
    elif action == "minus" and cart_item.quantity  > 0 :
        cart_item.quantity -= 1
        cart_item.total_price = cart_item.pet.price * cart_item.quantity
    cart_item.save()
    users_id=request.session.get('id')
    user= Users.objects.get(id=users_id)
    all_cart_of_a_user = Cart.objects.filter(user=user)
    for all_cart_of_a_user in all_cart_of_a_user:
        all_cart_of_a_user.grand_total = all_cart_of_a_user.total_price
    all_cart_of_a_user.save()
    return redirect('/cart/')     

def buyapet(request,id):
    pet=Cart.objects.get(id=id)
    return render(request,'checkout.html',{'pet':pet})


def buyallpets(request):
    users_id=request.session.get('id')
    user=Users.objects.get(id=users_id)
    pets=Cart.objects.filter(user=user)
    grand_total = sum(item.quantity * item.pet.price for item in pets)
    return render (request,'checkouts.html',{'pets':pets,'grand_total':grand_total})


def payment(request,amount):
    client=razorpay.Client(auth=('rzp_test_a8OmF04Ppiwsc6','3hH4nbEz5DKkBBzR1iLKZdt4'))
    response_payment=client.order.create(dict(amount=int(amount)*100,currency="INR"))
    print('response_payment',response_payment)
    return redirect('/orders/')


def success(request,amount,id,payment_id,address,session):
    user=Users.objects.get(id=session)
    pet=Cart.objects.get(id=id)
    subs=Payments.objects.create(user=user,amount=amount,pet=pet,payment_id=payment_id)
    subs.save()
    user_token=random.randint(1,10000)
    delivery_token=random.randint(1,10000)
    delivary_details=Delivery_details.objects.create(user=user,pet=pet,amount=amount,user_token=user_token,delivery_token=delivery_token,address=address,delivery_status='delivered')
    delivary_details.save()
    return redirect(f'/payment/{amount}/')


def orders(request):
    user_id=request.session.get('id')
    user=Users.objects.get(id=user_id)
    orders=Delivery_details.objects.filter(user=user)
    return render (request,'order.html',{'orders':orders})  