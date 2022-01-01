from os import name
from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from smartHome.models import Product
from django.shortcuts import redirect, render
from django.views import View
from .forms import CustomerProfileForm, CustomerRegisterForm
from django.contrib import messages
from django.views.generic import DetailView
from .models import Cart, Customer, OrderPlaced
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.


class ProductView(View):

    def get(self,request):
        homeAutomation = Product.objects.filter(category='HM')
        main_product1 = Product.objects.filter(category='HSS').filter(rating=9.9)
        cardBox1 = Product.objects.filter(category='HF')[:1]
        cardBox2 = Product.objects.filter(category='HM').filter(title__icontains='watering')
        trending_deals = Product.objects.filter(rating__gt=8.0)
        energy_mgt = Product.objects.filter(category='HEM')

        context = {
            'homeAutomation':homeAutomation,
            'cardBox1': cardBox1,
            'cardBox2': cardBox2,
            'energy_mgt': energy_mgt,
            'main_product':main_product1,
            'trending_deals':trending_deals,
        }

        return render(request,"smartHome/home.html",context)

@method_decorator(login_required, name='dispatch')
class ProductDetail(DetailView):

    def get(self, request,pk):
        product = Product.objects.get(pk=pk)
        item_already_there = False
        if request.user.is_authenticated:
            item_already_there = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        
        context = {
            "product":product,
            "item_already_there":item_already_there,
        }

        return render(request,"smartHome/product_detail.html",context)

@login_required
def devices_info(request, data=None):
    if data == None:
        devices = Product.objects.all()
    elif data == "HM":
        devices = Product.objects.filter(category=data)
    elif data == "HA":
        devices = Product.objects.filter(category=data)
    elif data == "HEM":
        devices = Product.objects.filter(category=data)
    elif data == "HSS":
        devices = Product.objects.filter(category=data)
    elif data == "HF":
        devices = Product.objects.filter(category=data)
    context = {
        "devices":devices,
    }

    return render(request,"smartHome/devices.html",context)

class CustomerRegisterView(View):

    def get(self,request):
        form = CustomerRegisterForm()
        context = {
            "form":form,
        }
    
        return render(request,"smartHome/customerRegister.html",context)

    def post(self,request):
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations! Registered Successfully')
            form.save()

        context = {
            "form":form,
        }
    
        return render(request,"smartHome/customerRegister.html",context)


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    
    def get(self,request):
        form = CustomerProfileForm()
        context = {
            "form":form,
            "active":'btn-dark',
        }

        return render(request,"smartHome/profile.html",context)

    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():

            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request,"Profile Has Been Updated.")

        context = {
            'form':form,
            "active":'btn-dark',
        }  

        return render(request,"smartHome/profile.html",context)

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)

    context = {
        "address":add,
        "active":'btn-dark',
    }

    return render(request,"smartHome/address.html",context)

@login_required
def add_to_cart(request):
    user = request.user
    product_slug = request.GET.get('product_id')
    product = Product.objects.get(id=product_slug)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amt = 69.0
        tot_amt = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamt = (p.quantity * p.product.discounted_price)
                amount += tempamt
                tot_amt = amount + shipping_amt 
        context = {
            "carts":cart,
            "totalamount": tot_amt,
            "amount":amount
        }
        return render(request,"smartHome/addToCart.html",context)


def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amt = 69.9
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamt = (p.quantity * p.product.discounted_price)
            amount += tempamt
            
        
        data = {
            "quantity":c.quantity,
            "amount":amount,
            "totalamount": amount + shipping_amt 
        }
    
        return JsonResponse(data)


def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amt = 69.9
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamt = (p.quantity * p.product.discounted_price)
            amount += tempamt
    
        
        data = {
            "quantity":c.quantity,
            "amount":amount,
            "totalamount":amount + shipping_amt 
        }
    
        return JsonResponse(data)


def remove_cart(request):
        if request.method == "GET":
            prod_id = request.GET['prod_id']
            c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            c.delete()
            amount = 0.0
            shipping_amt = 69.9
            cart_product = [p for p in Cart.objects.all() if p.user == request.user]
            for p in cart_product:
                tempamt = (p.quantity * p.product.discounted_price)
                amount += tempamt
                
            
            data = {
                "amount":amount,
                "totalamount":amount + shipping_amt
            }
        
            return JsonResponse(data)

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amt =  69.9
    tot_amt = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:       
        for p in cart_product:
            tempamt = (p.quantity * p.product.discounted_price)
            amount += tempamt
        tot_amt = amount + shipping_amt
    context = {
        "add":add,
        "totalamount":tot_amt,
        "cart_items":cart_items,
    }    
    return render(request,"smartHome/checkout.html",context)

@login_required
def payment_done(request):
    user = request.user
    cus_id = request.GET.get('custid')
    customer = Customer.objects.get(id=cus_id)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")
    

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request,"smartHome/orders.html",{"orders":op})

@login_required
def search_bar(request):
    query = request.GET['query']
    search_res = Product.objects.filter(title__icontains=query)
    context = {
        "results": search_res,
    }

    return render(request,"smartHome/search_bar.html",context)