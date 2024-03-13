from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control,never_cache
from django.contrib.auth import login as auth_login ,logout,authenticate
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError

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
        print(first_name)
        print(last_name)
        print(username)
        print(email)
        print(password)
        print(confirm_password)

        if not (username and email and password and confirm_password and first_name and last_name):
            messages.error(request, 'Please fill all the required fields.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        else:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
                return redirect('signup')
            else:
                try:
                    user = User.objects.create_user(username, email=email, password=password, first_name=first_name, last_name=last_name)
                    messages.success(request, 'Account created successfully. You can now log in.')
                    return redirect('login')
                except ValidationError as e:
                    messages.error(request, e.message_dict)
                    return redirect('signup')

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
            print(".......",username)
        

            if not username and password:
                messages.error(request,'please enter your username and password')
                return redirect('login')
            new = User.objects.get(email=username)
            print("new:",new)
            user=authenticate(request,username=new,password=password)
            print("---",user)
            if user is not None:
                request.session['username']=username
                auth_login(request,user)
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



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
def crudadmin(request):
    if 'username' in request.session:
        return redirect('home')
    if 'crud' in request.session:
        return redirect('dashboard')
    else:
        if request.method=='POST':
            uname=request.POST.get('username')
            passw=request.POST.get('password')
            print(uname,"-----")
            print(passw,"-----")
            new = User.objects.filter(email=uname).first()
            print("new",new)
            user=authenticate(request,username=new,password=passw)
            print("user",user)
            if user is not None and user.is_superuser:
                request.session['crud']=uname
                auth_login(request,user)
                return redirect('dashboard')
            else:
                messages.info(request,'invalid data')
    return render(request,'crudadmin.html')




@login_required(login_url='crud')
@login_required(login_url='login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
def dashboard(request):
    if 'crud' in request.session:
        users=User.objects.filter(is_staff=False)
        context={
            users:'users',
        }
        return render(request,'dashboard.html',context)
    return redirect('dashboard')

def add(request):
    if request.method=='POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
        user.save()
        return redirect('dashboard')
    return render(request,'dashboard.html')

def edit(request,id):
    des = des.objects.all()
    context = {
        'des' : des,
    }
    return render(request,'dashboard.html',context)

def update(request,id):
    user=User.objects.get(id=id)
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        user.username=name
        user.email=email
        user.password=password
        user.first_name=first_name
        user.last_name=last_name
        if password:
            user.set_password('password')
        user.save()
        return redirect('dashboard')
    else:
        context={
            'user':user,
        }
    return render(request,'dashboard.html',context)

def delete(request,id):
    des = User.objects.filter(id=id)
    des.delete()
    context ={
        'des':des,
    }
    return redirect(dashboard)

def search(request):
    query=request.GET.get('q')
    if query:
        results=User.objects.filter(username__icontains=query).exclude(username='admin')
    else:
        results=[]
    context={
        'results':results,
    }
    return render(request,'dashboard.html',context)


@login_required(login_url='login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache

def admin_logout(request):
    if 'crud' in request.session:
        del request.session['crud']
        auth.logout(request)
    return redirect('crud')