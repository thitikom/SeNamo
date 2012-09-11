__author__ = 'wattanai' #for every function for backOffice system

from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from app.models import Product, Category
from django.http import HttpResponse, HttpResponseRedirect
from app.forms import *
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User

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
                    #messages.add_message(request, messages.INFO, 'Successfully Logged in.')
                    return HttpResponseRedirect('/backoffice/managestock')
                else:
                    errorMess = 'Your account is inactive or you not have Employee permission role. Please contact Administrator.'
                    #messages.add_message(request, messages.ERROR, 'Your account is inactive or you not have Employee permission role. Please contact Administrator.')
            else:
                errorMess = 'Incorrect username or password.'
                #messages.add_message(request, messages.ERROR, 'Incorrect username or password.')
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

def managestock(request):
    return render_to_response('managestock.html')