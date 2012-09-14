__author__ = 'wattanai' #for every function for backOffice system


import datetime
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from app.models import Product, Category
from django.http import HttpResponse, HttpResponseRedirect
from app.forms import *
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def login(request):
    context = RequestContext(request,
        {
            'form' : loginEmp_form(),
        }
    )
    if request.method == 'POST':
        loginForm = loginEmp_form(request.POST)
        #data = loginForm.data
        if loginForm.is_valid():
            data = loginForm.cleaned_data
            username = data['username']
            password = data['password']

            user = auth.authenticate(username=username, password=password) # check if exist in DB
            if user is not None:
                if user.is_active and user.groups.filter(name = 'Employee'):
                    auth.login(request, user)
                    return HttpResponseRedirect('/backoffice/managestock')
                else:
                    errorMess = 'Your account is inactive or you not have Employee permission role. Please contact Administrator.'
            else:
                errorMess = 'Incorrect username or password.'
            context.update(
                {
                    'error': errorMess
                }
            )
            return render_to_response('login_employee.html',context )

        else:
            context.update(
                {
                    'error': 'Please fill all information'
                }
            )
            return render_to_response('login_employee.html',context )

    else:
        return render_to_response('login_employee.html',context)

@login_required(redirect_field_name='/backoffice/managestock', login_url='/backoffice/login')
def managestock(request):
    user = request.user
    emp = user.get_profile()
    is_manager = emp.manager
    if not is_manager:
        return packing(request)

    is_clerk = emp.clerk

    product_list = Product.objects.all().order_by('amount')
    list = []
    for product in product_list:
        if product.amount == 0:
            if product.orderSupStatus == True:
                list.append((product.id ,product.name, product.category.name, product.amount, product.orderSupStatus,'T'))
            else:
                list.append((product.id ,product.name, product.category.name, product.amount, product.orderSupStatus,))
        else:
            list.append((product.id, product.name, product.category.name, product.amount))

    dataContext = RequestContext(request,
        {
            'fullname' : user.get_full_name(),
            'manager' : 'Manager',
            'product_list' : list,
        }
    )
    if is_clerk:
        dataContext.update({'clerk':'Clerk'})

    return render_to_response('managestock.html',dataContext)

@login_required(redirect_field_name='/backoffice/managestock', login_url='/backoffice/login')
def increaseStock(request,prod_id):
    if request.method == 'POST':
        product = get_object_or_404(Product,id=prod_id)
        newAmount = request.POST.get('amount')
        newStatus = request.POST.get('ordered')
        product.amount = newAmount
        if newStatus != None:
            product.orderSupStatus = True
        else:
            product.orderSupStatus = False
        product.save()

        productIncreased = ProductInOrder.objects.filter(product = product)
        for pInc in productIncreased:
            order = pInc.order
            if order.status != 'Shipped':
                order.status = 'products now instock'
                order.save()

    return HttpResponseRedirect('/backoffice/managestock')

@login_required(redirect_field_name='/backoffice/managestock', login_url='/backoffice/login')
def managecatalog(request, category_id=0):
    user = request.user
    emp = user.get_profile()
    is_manager = emp.manager
    if not is_manager:
        return packing(request)

    categories = Category.objects.all()

    if category_id != 0:
        product_list = Product.objects.filter(category__id = category_id)
    else:
        product_list = Product.objects.all().order_by('category')

    is_clerk = emp.clerk
    dataContext = RequestContext(request,
        {
            'fullname' : user.get_full_name(),
            'manager':'Manager',
            'categories' : categories,
            'product_list' : product_list
        }
    )
    if is_clerk:
        dataContext.update({'clerk':'Clerk'})

    return render_to_response('managecatalog.html',dataContext)

@login_required(redirect_field_name='/backoffice/packing', login_url='/backoffice/login')
def packing(request):
    user = request.user
    emp = user.get_profile()
    is_manager = emp.manager
    is_clerk = emp.clerk
    if not is_clerk:
        return managestock(request)

    order_list = Order.objects.exclude(status='Shipped')

    dataContext = RequestContext(request,
        {
            'fullname' : user.get_full_name(),
            'clerk':'Clerk',
            'list': order_list,
        }
    )
    if is_manager:
        dataContext.update({'manager':'Manager', })

    return render_to_response('packing.html',dataContext)

@login_required(redirect_field_name='/backoffice/packing', login_url='/backoffice/login')
def proceedPacking(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order,id=order_id)
        ordered_product_list = ProductInOrder.objects.filter(order = order)
        for ordered_product in ordered_product_list:
            if ordered_product.ship_time == None:
                updateStat = request.POST.get(ordered_product.product.name)
                if updateStat == 'send':
                    ordered_product.ship_time = datetime.datetime.now()
                    ordered_product.save()
                    upAmountProduct = ordered_product.product
                    upAmountProduct.amount = upAmountProduct.amount - ordered_product.amount
                    upAmountProduct.save()
                    print(upAmountProduct.amount)

        review_product_list = ProductInOrder.objects.filter(order = order)
        shipped = True
        for review_product in review_product_list:
            if review_product.ship_time == None:
                order.status = 'Wait for more products'
                shipped = False

        if shipped:
            order.status = 'Shipped'

        order.save()

        return HttpResponseRedirect('/backoffice/packing')

    else:
        order = get_object_or_404(Order,id=order_id)
        ordered_product_list = ProductInOrder.objects.filter(order = order)
        list = []
        i = 1
        for ordered_product in ordered_product_list:
            if ordered_product.ship_time != None:
                list.append((i,ordered_product.product.name, ordered_product.amount, ordered_product.ship_time))
            else:
                list.append((i,ordered_product.product.name, ordered_product.amount))
            i = i+1

        dataContext = RequestContext(request,
            {
                'order_id' : order.id,
                'order_date' : order.timestamp,
                'name' : order.user.get_full_name(),
                'email' : order.user.email,
                'address' : order.get_address(),
                'tel' : order.user.get_profile().tel,
                'ordered_product_list' : list,
            }
        )
        return render_to_response('packingDetail.html', dataContext)