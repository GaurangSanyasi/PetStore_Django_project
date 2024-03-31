from django.shortcuts import render, HttpResponseRedirect
from .models import Product, Cart, Address
from .forms import ProductForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def Index(request):
    if request.method == 'POST':
        fm = ProductForm(request.POST,request.FILES)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect('/display/')
            fm = ProductForm()
    else:
        fm = ProductForm()

    return render(request,'index.html',{'form':fm})

def display(request):
    data = Product.objects.all()
    return render(request,'display.html',{'data':data})

def Delete(request,id):
    if request.method == 'POST':
        os = Product.objects.get(pk = id)
        os.delete()
        return HttpResponseRedirect('/display/')
    
def Update(request,id):
    if request.method == "POST":
        os = Product.objects.get(pk=id)
        fm = ProductForm(request.POST, request.FILES, instance=os)
        if fm.is_valid():
            fm.save()
            messages.success(request,"Data Updated Succesfully")
            return HttpResponseRedirect('/display/')
    else:
        os = Product.objects.get(pk=id)
        # print(os)
        fm = ProductForm(instance=os)
    return render(request, 'update.html',{'Updateform':fm})

def UserBase(request):
    if request.user.is_authenticated:
        count = Cart.objects.all().count()
        return render(request, 'user/base.html',{'count':count})
    else:
        return HttpResponseRedirect('/')

def UserIndex(request):
    if request.user.is_authenticated:
        data = Product.objects.all()
        count = Cart.objects.filter(user_id=request.user).count()
        return render(request, 'user/index.html',{'data':data, 'count':count})
    else:
        return HttpResponseRedirect('/')

def AddToCart(request):
    if request.user.is_authenticated:
        if request.method =='POST':
            cid = request.POST.get('cid')
            filter1 = Cart.objects.all().values_list('product_id', flat=True)
            if int(cid) not in filter1:
                Cart.objects.create(product_id=cid, user = request.user)
                return HttpResponseRedirect('/cart/')
            else:
                messages.success(request, 'This Product Is Already Added In Cart')
        cid = Cart.objects.filter(user_id=request.user).values_list('product_id',flat=True)
        cartdata = Product.objects.filter(id__in=cid)
        amount = Product.objects.filter(id__in=cid).values_list('price',flat=True)
        amt = 0
        for i in amount:
            amt+=i
        return render(request,'user/cart.html',{'cdata':cartdata,'amt':amt})
    else:
        return HttpResponseRedirect('/')

def RemoveCart(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            Cart.objects.filter(product_id=id).delete()
            return HttpResponseRedirect('/cart/')
    else:
        return HttpResponseRedirect('/')

def SearchComponents(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                search = request.POST.get('search')
                Sdata = Product.objects.filter(Q(category=search) | Q(pname=search) | Q(desc__icontains=search) |Q(price__contains=search))
            return render(request, 'user/search.html',{'sdata':Sdata})
        except:
            return HttpResponseRedirect('/userindex/')
    else:
        return HttpResponseRedirect('/')
    
def Details(request,id):
    if request.user.is_authenticated:
        data_details = Product.objects.filter(pk=id)
        return render(request, 'user/details.html',{'data':data_details})
    else:
        return HttpResponseRedirect('/')
def SignUp(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass')
        User.objects.create_user(uname,email,pass1)
        messages.success(request, 'SignUp succesfull')
    return render(request, 'user/signup.html')

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/userindex/')
    return render(request, 'user/login.html')

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def address(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            cname = request.POST.get('cname')
            flat = request.POST.get('flat')
            landmark = request.POST.get('landmark')
            city = request.POST.get('city')
            state = request.POST.get('state')
            pincode = request.POST.get('pincode')
            contact = request.POST.get('contact')
            acontact = request.POST.get('acontact')
            print(cname,flat,city,state,pincode,contact,acontact)

            Address.objects.create(user=request.user, name=cname,flat=flat,landmark=landmark,city=city,state=state,pincode=pincode,contact=contact,contactA=acontact)
        data = Address.objects.filter(user_id = request.user)
        return render(request, 'user/address.html',{'adata':data})
    else:
        return HttpResponseRedirect('/')

