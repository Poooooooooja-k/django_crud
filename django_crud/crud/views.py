from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control,never_cache
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def signup(request):
    if 'username' in request.session:
        return redirect('home')
    elif request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')

        if not (username and email and password and confirm_password and first_name and last_name):
            messages.error(request, 'Please fill all the required fields.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        else:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                user.save()
                messages.success(request, 'Account created successfully. You can now log in.')
                return redirect('login')
    return render(request, 'signup.html')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
def login(request):
    if 'username' in request.session:
        return redirect('home')
    else:
        if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')

            if not username and password:
                messages.error(request,'please enter your username and password')
                return redirect('login')
            user=auth.authenticate(username=username,password=password)
            if user is not None:
                request.session['username']=username
                login(request,user)
                return redirect('home')
            else:
                user_exists=User.objects.filter(username=username).exists()
                if user_exists:
                    messages.error(request,'incorrect password!!')
                else:
                    messages.error(request,'incorrect username or password!!')
                return redirect('login')
        else:
            return render(request,'login.html')
        

def logout(request):
    if 'username' in request.session:
        del request.session['username']
        auth.logout(request)
        return redirect('login')
    
    return redirect('login')


@login_required(login_url='login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def home(request):
    return render(request,'home.html')


def crudadmin(request):
    return render(request,'crudadmin.html')



def dashboard(request):
    return render(request,'dashboard.html')

