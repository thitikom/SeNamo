__author__ = 'wattanai' #for every function for backOffice system

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
            #form = stockEmpty_manage_form(initial={'amount':product.amount, 'status':product.orderSupStatus})
            if product.orderSupStatus == True:
                list.append((product.id ,product.name, product.category.name, product.amount, product.orderSupStatus,'T'))
            else:
                list.append((product.id ,product.name, product.category.name, product.amount, product.orderSupStatus,))
        else:
            #form = stockNormal_manage_form(initial={'amount':product.amount})
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
    return HttpResponseRedirect('/backoffice/managestock')

@login_required(redirect_field_name='/backoffice/managestock', login_url='/backoffice/login')
def managecatalog(request):
    user = request.user
    emp = user.get_profile()
    is_manager = emp.manager
    if not is_manager:
        return packing(request)

    is_clerk = emp.clerk
    dataContext = RequestContext(request,
        {
            'fullname' : user.get_full_name(),
            'manager':'Manager'
        }
    )
    if is_clerk:
        dataContext.update({'clerk':'Clerk'})

    return render_to_response('managecatalog.html',dataContext)

@login_required(redirect_field_name='/backoffice/managestock', login_url='/backoffice/login')
def packing(request):
    user = request.user
    emp = user.get_profile()
    is_manager = emp.manager
    is_clerk = emp.clerk
    if not is_clerk:
        return managestock(request)

    dataContext = RequestContext(request,
        {
            'fullname' : user.get_full_name(),
            'clerk':'Clerk'
        }
    )
    if is_manager:
        dataContext.update({'manager':'Manager', })

    return render_to_response('packing.html',dataContext)