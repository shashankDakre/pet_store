from django.shortcuts import render, redirect
from account.models import Users, Profile_pic
from account.models import Profile_pic
from django.contrib import messages
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password

def register(request):
    if request.method=="POST":
        name=request.POST['name']
        mobile = request.POST['mobile']
        email = request.POST['email']
        city = request.POST['city']
        state = request.POST['state']
        address = request.POST['address']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if confirm_password == password:
            if Users.objects.filter(email=email).exists():
                messages.info(request,'Email exists')
                return redirect('/account/register/')
            elif Users.objects.filter(mobile=mobile).exists():
                messages.info(request,'Number already Exists')
                return redirect('/account/register/')
            else:
                password = make_password(password)
                customer = Users.objects.create(name=name,email=email,state=state,city=city,address=address,mobile=mobile,password=password)
                customer.save()
                return redirect('/account/login/')
        else:
            messages.info(request,'Password and confirm password does not match')
            return redirect('/account/register')
    return render(request, 'register.html')

def login(request):
    if request.method=="POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            customer = Users.objects.get(email=email)
            if customer.email == (email) and check_password(password,customer.password):
                request.session['id']=customer.id
                return redirect('/pet/')
            else:
                messages.info(request,'Invalid Credentials')
                return redirect('/account/login/')         
        except ObjectDoesNotExist:
            messages.info(request,'Mobile does not exists')
            return redirect('/account/login/')      
    return render(request, 'login.html')

def logout(request):
    user = request.session.get('id')
    user.session.flush()
    return redirect('/login/')

def profile_pic(request,id):
    if request.method=="POST":
      profile_pics=request.FILES.get("profile_pic")
      user_id = request.session.get('id')
      try:
          user = Users.objects.get(id=user_id)
          profile_picture,created = Profile_pic.objects.get_or_create(user=user)
          profile_picture.profile_pic= profile_pics
          profile_picture.save()
      except Users.DoesNotExist:
          return redirect("/profile/")   
    return redirect('/profile/')

# def logout_view(request):
#     # Logic for handling registration
#     return render(request, 'login.html', {'login':login_view})

def delete_profile(request,id):
    image = Profile_pic.objects.get(id=id)
    image.delete()
    return redirect ('/profile/')