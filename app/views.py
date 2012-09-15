from _ast import excepthandler
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from app.models import *
from django.http import HttpResponse, HttpResponseRedirect
from app.forms import *
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import requests

def index(request):
    product_list = Product.objects.all()
    category_list = Category.objects.all()
    context = RequestContext(request,{
        'product_list':product_list,
             })
    #context['category_list'] = category_list
    c = RequestContext(request,context)
    return render_to_response('catalog_view.html',context)

def search(request):
    if request.method == 'GET':
        q = request.GET.get('q')
        product_list = Product.objects.filter(name__icontains=q)
        context = RequestContext(request,{'product_list':product_list,
                                          'q':q})
        return render_to_response('search.html',context)

def view_category(request, category_id):
    products_list = Product.objects.filter(category__id = category_id).order_by('name')[:10]
    category_detail = get_object_or_404(Category, id=category_id)
    context = RequestContext(request,{
        'products_list': products_list,
        'category_detail': category_detail,
        })
    return render_to_response('view_category.html',context)
    #    return HttpResponse("You're looking at category %s." % category_id)

def view_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    category_detail = get_object_or_404(Category, id=product.category.id)
    return render_to_response('view_product.html',
        context_instance=RequestContext(request,{
            'messages': messages,
            'product': product,
            'category_detail': category_detail,
            }))

#update context of forms
def update_product_context(context, data, error_type, error_msg):
    context.update({
        'form': add_product_form(
            initial={'name':data['name'], 'price':data['price'], 'point':data['point'],
                     'category':data['category'], 'description':data['description'],
                     'image':data['image']}
        ),
        error_type: error_msg
    })
    return context

def add_product(request):
    context = RequestContext(request, {'form': add_product_form()})

    if request.method == 'POST':
        apf = add_product_form(request.POST, request.FILES)
        data = apf.data

        if apf.is_valid():
            data = apf.cleaned_data

            if data['image'] is not None:
                file_type = data['image'].content_type.split('/')[0]
                if file_type != 'image':
                    context.update({
                        'form': add_product_form(
                            initial = {
                                'name': data['name'],
                                'price': data['price'],
                                'point': data['point'],
                                'category': data['category'],
                                'description': data['description'],
                                'supplier': data['supplier'],
                                'amount': data['amount'],
                                'orderSupStatus': data['orderSupStatus'],
                            }
                        ),
                        'file_type_error_msg': 'Image File Only !!',
                    })
                    return render_to_response('add_product.html', context)

            product = Product.objects.get_or_create(
                name = data['name'],
                price = data['price'],
                point = data['point'],
                category = data['category'],
                description = data['description'],
                supplier = data['supplier'],
                image = request.FILES['image']
            )[0]
            product.save()
            context.update(
                {'form': add_product_form, 'success_msg': 'Product successfully created.'}
            )
            return HttpResponseRedirect('/backoffice/managecatalog')
        else:
            context.update({
                'form': add_product_form(
                    initial = {
                        'name': data['name'],
                        'price': data['price'],
                        'point': data['point'],
                        'category': data['category'],
                        'description': data['description'],
                        'supplier': data['supplier'],
                    }
                ),
                'form_error_msg': 'Please fill all required information'
            })

    return render_to_response('add_product.html', context)

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method =='GET':
        apf = add_product_form(instance=product)
        return render_to_response('edit_product.html', RequestContext(request, {'form': apf, 'pid': product_id, 'product': product}))
    else:
        apf = add_product_form(request.POST, instance=product)
        if apf.is_valid():
            apf.save()
        else:
            apf = add_product_form(instance=product)

        return HttpResponseRedirect('/backoffice/managecatalog')

def add_category(request):
    context = RequestContext(request, {'form': add_category_form})

    if request.method == 'POST':
        acf = add_category_form(request.POST)
        data = acf.data

        if acf.is_valid():
            data = acf.cleaned_data
            category = Category.objects.get_or_create(name=data['name'], description=data['description'])[0]
            category.save()
            context.update(
                    {'form': add_category_form, 'success_msg': 'category successfully created'}
            )
            return HttpResponseRedirect('/backoffice/managecatalog')
        else:
            context.update({
                'form': add_category_form(
                    initial={'name': data['name'], 'description': data['description']}
                ),
                'form_error_msg': 'please fill all required information'
            })
            return render_to_response('add_category.html', context)
    else:
        return render_to_response('add_category.html', context)

def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    context = RequestContext(request, {'form': add_category_form()})

    if request.method == 'GET':
        context = RequestContext(request, {
            'form': add_category_form(
                initial={'name': category.name, 'description': category.description}
            ),
            'cid': category.id
        })
        return render_to_response('edit_category.html', context)
    else:
        acf = add_category_form(request.POST)
        data = acf.data

        if acf.is_valid():
            data = acf.cleaned_data
            category.name = data['name']
            category.description = data['description']
            category.save()
            return HttpResponseRedirect('/backoffice/managecatalog')
        else:
            context.update({
                'form': add_category_form(
                    initial={'name': data['name'], 'description': data['description']}
                ),
                'form_error_msg': 'please fill all required informations',
                'cid': category.id
            })
            return render_to_response('edit_category.html', context)

def delete_product(request, product_id):
    product = get_object_or_404(Product,id=product_id)
    product.delete()

    messages.add_message(request,messages.SUCCESS,'Successfully delete product.')
    context = RequestContext(request, {
        messages : messages
    })
    return render_to_response('delete_record.html',context)

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()

    messages.add_message(request, messages.SUCCESS, 'Successfully delete category.')
    context = RequestContext(request, {
        messages : messages
    })
    return HttpResponseRedirect('/backoffice/managecatalog')

def register_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.method=="POST" :
            form = RegisterForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']
                user = User.objects.create_user(username,email,password)
                messages.add_message(request, messages.SUCCESS, "You've successfully registered.")
                context = RequestContext(request,{
                    'messages' : messages
                })
                return HttpResponseRedirect('/login')
            else:
                messages.add_message(request, messages.ERROR, "You've enter invalid information.")
                context = RequestContext(request,{
                    'form' : RegisterForm()
                })
                return render_to_response('register_user.html',context)
        else:
            context = RequestContext(request,{
                'form' : RegisterForm()
            })
            return render_to_response('register_user.html',context)

def login(request):
    if request.user.is_authenticated():
        if request.method == 'GET' and request.GET.get('next'):
            HttpResponseRedirect(request.GET['next'])
        else:
            return HttpResponseRedirect('/')
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password) # check if exist in DB
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                messages.add_message(request, messages.INFO, 'Successfully Logged in.')
            else:
                messages.add_message(request, messages.ERROR, 'Your account is inactive. Please contact Administrator.')
        else:
            messages.add_message(request, messages.ERROR, 'Incorrect username or password.')

        if request.POST.get('next') and user is not None:
            return HttpResponseRedirect(request.POST['next'])
        elif user is not None:
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/login')

    if request.method == 'GET' and request.GET.get('next'):
        context = RequestContext(request, {
            'messages': messages, 'next': request.GET['next']})
    else:
        context = RequestContext(request, {
            'messages': messages})
    return render_to_response('login_user.html',context)

#private method
def calc_price_point(request):
    if not request.session.get('product_in_cart'):
        request.session['product_in_cart'] = []
    cart_list = request.session['product_in_cart']
    total_price = 0
    total_point = 0
    if len(cart_list) != 0:
        for product in cart_list:
            total_price += int(product[2])
            total_point += int(product[3])
    return (total_price,total_point)

def view_cart(request):
    user = request.user;
    (total_price,total_point) = calc_price_point(request)
    context = RequestContext(request, {'product_in_cart': request.session['product_in_cart'],
                                       'total_price':total_price,
                                       'total_point':total_point,
                                       'username':user.get_profile,
                                       })
    return render_to_response('view_cart.html',context)

def add_session(request):
    if not request.session.get('product_in_cart'):
        request.session['product_in_cart'] = []
    tmp = request.session['product_in_cart']
    tmp.append(2)
    tmp.append(3)
    tmp.append(4)
    request.session['product_in_cart'] = tmp
    context = RequestContext(request, {'product_in_cart': request.session['product_in_cart']})
    return render_to_response('view_cart.html',context)
@login_required()
def add_cart(request,product_id):
    product_amount = 0
    if not request.session.get('product_in_cart'):
        request.session['product_in_cart'] = []
    if request.method == 'POST':
        product_amount = request.POST.get('amount')
        added_product = (Product.objects.get(id=product_id),product_amount,
                         int(product_amount)*int(Product.objects.get(id=product_id).price),
                         int(product_amount)*int(Product.objects.get(id=product_id).point))
        tmp = request.session['product_in_cart']
        tmp.append(added_product)
        request.session['product_in_cart'] = tmp
        messages.add_message(request, messages.INFO, 'Successfully Added to cart.')
    return HttpResponseRedirect("/product/"+product_id)

def clear_cart(request):
    request.session['product_in_cart'] = []
    return HttpResponseRedirect("/")

def view_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.user != order.user:
        messages.add_message(request, messages.ERROR, "You don't have permission to view this order.")
        if request.GET.get('next'):
            return HttpResponseRedirect(request.GET['next'])
        else:
            return HttpResponseRedirect('/')
    else:
        products_list = ProductInOrder.objects.filter(order__id = order_id).order_by('product')
        list = []
        total_price = 0
        total_point = 0
        for product_io in products_list:
            price = int(product_io.product.price) * int(product_io.amount)
            point = int(product_io.product.point) * int(product_io.amount)
            list.append((product_io, price, point))
            total_price += price
            total_point += point
    context = RequestContext(request,{
        'order': order,
        'products_list': list,
        'total_price': total_price,
        'total_point': total_point,
        'username':request.user,
        })
    return render_to_response('view_order_detail.html',context)

#Checkout
def verify(card_no,ccv,total_price):
    if card_no and ccv == '123':
        return 'success'

    params = {
        'card_num' : card_no,
        'card_ccv' : ccv,
        'amount' : total_price
    }

    url = settings.BANK_URL
    response = requests.post('%s/verify' % url,params)
    return response.content

def pay(card_no,ccv,total_price):
    if card_no and ccv == '123':
        return 'success'

    params = {
        'card_num' : card_no,
        'card_ccv' : ccv,
        'amount' : total_price
    }

    url = settings.BANK_URL
    response = requests.post('%s/pay' % url,params)
    return response.content
def show_card_no(card_no):
    if len(card_no) >= 16:
        return "####-####-####-" + card_no[12:16]
    else:
        return card_no

@login_required
def checkout_payment(request):
    user = request.user
    user_profile = user.get_profile()
    (total_price,total_point) = calc_price_point(request)
    if not total_point and not total_price:
        messages.add_message(request, messages.ERROR, 'Cannot checkout! nothing in cart.')
        return HttpResponseRedirect('/cart')
    if request.method == 'GET':
        context = RequestContext(request, {'form': credit_card_form(),
                                           'oldcard': show_card_no(user_profile.creditcard),
                                           'total_price': total_price,
                                           'total_point': total_point,
                                           'username':request.user,
                                           })
        return render_to_response('checkout_payment.html',context)
    else: #POST
        select_card = request.POST.get('select_card')
        if not select_card:
            messages.add_message(request, messages.ERROR, 'Please select credit card')
            return HttpResponseRedirect('/checkout/payment')
        ccv = request.POST.get('ccv')
        if not ccv:
            messages.add_message(request, messages.ERROR, 'Please enter correct ccv number')
            return HttpResponseRedirect('/checkout/payment')

        if select_card == 'old':
            card_no = user_profile.creditcard
        else:
            card_no = request.POST.get('card_number')
            if not card_no:
                messages.add_message(request, messages.ERROR, 'Please enter credit card number')
                return HttpResponseRedirect('/checkout/payment')

        #verify total point
        if total_point > user_profile.point:
            messages.add_message(request, messages.ERROR, 'Not enough points, you got %d pts.'%(user_profile.point))
            return HttpResponseRedirect('/cart')

        #verify card_no ccv total_price with bank
        v = verify(card_no,ccv,total_price)
        if v == 'success':
            messages.add_message(request, messages.INFO, 'Payment accepted')
            request.session['checkout'] = {'card_no': card_no,
                                          'ccv' : ccv,
                                          'total_price' : total_price,
                                          'total_point' : total_point,}
            return HttpResponseRedirect('/checkout/shipping')
        else:
            messages.add_message(request, messages.ERROR, 'Payment rejected by bank')
            return HttpResponseRedirect("/checkout/payment")

@login_required(redirect_field_name='/cart')
def checkout_shipping(request):
    checkout = request.session['checkout']
    if not checkout:
        return HttpResponseRedirect("/checkout/payment")
    user = request.user
    user_profile = user.get_profile()
    if request.method == 'GET':
        (total_price,total_point) = calc_price_point(request)
        #print user_profile.get_address()
        context = RequestContext(request, {'form': address_form(),
                                           'oldaddress': user_profile.get_address(),
                                           'total_price': total_price,
                                           'total_point': total_point,
                                           'username':user_profile,
                                           })
        return render_to_response('checkout_shipping.html',context)

    else: #POST
        select_address = request.POST.get('select_address')
        if not select_address:
            messages.add_message(request, messages.ERROR, 'Please select shipping address')
            return HttpResponseRedirect('/checkout/shipping')

        if select_address == 'old':
            address = user_profile.get_address()
        else:
            address = {}
            address['firstline'] = request.POST.get('first_line')
            address['secondline'] = request.POST.get('second_line')
            address['town'] = request.POST.get('town')
            address['country'] = request.POST.get('country')
            address['zipcode'] = request.POST.get('zip_code')

            if not (address['zipcode'] and address['country'] and address['town'] and address['firstline']):

                messages.add_message(request, messages.ERROR, 'Please enter address')
                return HttpResponseRedirect('/checkout/shipping')

        #messages.add_message(request, messages.INFO, 'Your order is placed')

        request.session['checkout']['address'] = address
        request.session.modified = True

        return HttpResponseRedirect('/checkout/finish')


def checkout_finish(request):
    user = request.user
    user_profile = user.get_profile()
    checkout = request.session['checkout']
#    if True:
#        return HttpResponse(repr(checkout))
    address = checkout['address']

    if not address:
        return HttpResponseRedirect("/checkout/payment")
    card_no = checkout['card_no']
    ccv = checkout['ccv']
    total_price = checkout['total_price']
    total_point = checkout['total_point']
    product_list = request.session['product_in_cart']

    fraud = ((not (total_price,total_point) == calc_price_point(request) )
             or total_point > user_profile.point
             or (not verify(card_no,ccv,total_price)=='success'))

    if fraud:
        messages.add_message(request, messages.ERROR, 'FRAUD DETECTED!!')
        return HttpResponseRedirect('/checkout/problem')

    pay(card_no,ccv,total_price)

    #deduct points
    user_profile.point -= total_point
    user_profile.creditcard = card_no
    user_profile.addr_firstline = address['firstline']
    user_profile.addr_secondline = address['secondline']
    user_profile.addr_town = address['town']
    user_profile.addr_country = address['country']
    user_profile.addr_zipcode=address['zipcode']
    user_profile.save()

    #create order
    order = Order.objects.create(user=user,status='placed',
        total_price = total_price,
        total_point = total_point,
        addr_firstline = address['firstline'],
        addr_secondline=address['secondline'],
        addr_town=address['town'],
        addr_country=address['country'],
        addr_zipcode=address['zipcode'])

    for product_tuple in product_list:
        (product,amount,x,y) = product_tuple
        ProductInOrder.objects.create(product=product,amount=amount,
                                        status='placed',order=order)

    request.session['checkout'] = {}
    request.session['product_in_cart'] = []
    context = RequestContext(request,{'order':order})
    return render_to_response('checkout_finish.html',context)

def checkout_problem(request):
    request.session['checkout'] = None
    return render_to_response('problem.html',RequestContext(request))

def view_order_history(request):
    user_account = request.user
    order_list = Order.objects.filter(user=user_account).order_by('timestamp')
    context = RequestContext(request,{
        'order_list':order_list,
        'messages':messages,
        'username':user_account,
    })
    return render_to_response('view_order_history.html',context)


def add_supplier(request):
    context = RequestContext(request, { 'form': add_supplier_form() })

    if request.method == 'POST':
        asf = add_supplier_form(request.POST)
        data = asf.data

        if asf.is_valid():
            data = asf.cleaned_data
            supplier = Supplier.objects.get_or_create(company_name=data['company_name'], contact=data['contact'])[0]
            supplier.save()
            context.update(
                {'form': add_supplier_form, 'success_msg': 'Supplier successfully created.'}
            )
        else:
            context.update({
                'form':add_supplier_form(
                    initial = {'company_name': data['company_name'], 'contact': data['contact']}
                ),
                'form_error_msg': 'please fill all required information'
            })

    return render_to_response('add_supplier.html', context)

def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)

    if request.method == 'GET':
        asf = add_supplier_form(instance=supplier)
        return render_to_response('edit_supplier.html', RequestContext(request, {'form': asf, 'sid': supplier_id}))
    else:
        asf = add_supplier_form(request.POST, instance=supplier)
        if asf.is_valid():
            asf.save()
        else:
            asf = add_supplier_form(instance=supplier)

        return HttpResponseRedirect('/supplier/%d' % supplier.id)

def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier,id=supplier_id)
    supplier.delete()

    messages.add_message(request,messages.SUCCESS,'Successfully delete supplier.')
    context = RequestContext(request, {
        messages : messages
    })
    return render_to_response('delete_record.html',context)

def view_supplier(request):
    supplier_list = Supplier.objects.order_by('company_name')
    context = RequestContext(request, {
        'supplier_list' : supplier_list,
        'messages' : messages
    })
    return render_to_response('view_supplier.html',context)

def view_order_to_deliver(request):
    order_list = Order.objects.exclude(status='Shipped')
    return render_to_response('packing.html', {'list': order_list})

#Arm Edit
@login_required()
def edit_profile(request):
    user_account = request.user
    profile = get_object_or_404(UserProfile,user=user_account)
    if request.POST :
        form = add_profile_form(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Update User's Profile
            user = profile.user
            if data['is_change_password']:
                user.set_password(data['new_password'])
            user.email = data['email']
            user.first_name = data['first_name']
            user.last_name = data['last_name']

            profile.birthday = data['birth_date']
            profile.sex = data['sex']
            profile.creditcard = data['creditcard']

            profile.save()
            user.save()

            # Update Address
            address = address_form(request.POST).data;
            profile.addr_firstline  = address['first_line']
            profile.addr_secondline = address['second_line']
            profile.addr_town       = address['town']
            profile.addr_country    = address['country']
            profile.addr_zipcode    = address['zip_code']
            profile.save()
            messages.add_message(request, messages.ERROR, "Profile edited.")
            return HttpResponseRedirect('/profile/')
        else:
            data = form.data
            address = address_form(request.POST).data;
            CHOICES = (('0', 0), ('1', 1), ('2', 2),)
            data['sex'] = dict(CHOICES)[data['sex']]
            #context = RequestContext(request, { 'form': add_profile_form(request.POST) })
            try:
                birthday = data['birth_date']
                bday = str(birthday.year)+'-'+str(profile.birthday.month)+'-'+str(profile.birthday.day);
            except AttributeError:
                bday = data['birth_date']
                # to print form.field.errors in template old form needed --noly
            #            context = RequestContext(request, {'form':form})
#            messages.add_message(request, messages.ERROR, "You've enter invalid information.")
            for error_mess in form.errors:
                messages.add_message(request, messages.ERROR, form.errors[error_mess][0])
#            messages.add_message(request, messages.ERROR, form._errors['email'][0])
#            messages.add_message(request, messages.ERROR, form._errors['creditcard'][0])
#            messages.add_message(request, messages.ERROR, form._errors['old_password'][0])
#            messages.add_message(request, messages.ERROR, form._errors['confirm_password'][0])
            context = RequestContext(request, {
                'messages': messages,
                'form':{
                    'username':user_account,
                    'age':profile.get_age(),
                    'checked_undefined':"""checked=checked""" if data['sex'] == 0 else '',
                    'checked_male':"""checked=checked""" if data['sex'] == 1 else '',
                    'checked_female':"""checked=checked""" if data['sex'] == 2 else '',
                    'tel':data['tel'],
                    'email':data['email'],
                    'first_name':data['first_name'],
                    'last_name':data['last_name'],
                    'birth_date':bday,
                    'creditcard':data['creditcard'],
                    'first_line':address['first_line'],
                    'second_line':address['second_line'],
                    'town':address['town'],
                    'country':address['country'],
                    'zip_code':address['zip_code'],
                }})
            return render_to_response('edit_profile.html', context)
    else:
        try:
            bday = str(profile.birthday.year)+'-'+str(profile.birthday.month)+'-'+str(profile.birthday.day);
        except AttributeError:
            bday = ''
        context = RequestContext(request, {
            'messages': messages,
            'form':{
                'username':user_account,
                'age':profile.get_age(),
                'checked_undefined':"""checked=checked""" if profile.sex == 0 else '',
                'checked_male':"""checked=checked""" if profile.sex == 1 else '',
                'checked_female':"""checked=checked""" if profile.sex == 2 else '',
                'tel':profile.tel,
                'email':profile.user.email,
                'first_name':profile.user.first_name,
                'last_name':profile.user.last_name,
                'birth_date':bday,
                'creditcard':profile.creditcard,
                'first_line':profile.addr_firstline,
                'second_line':profile.addr_secondline,
                'town':profile.addr_town,
                'country':profile.addr_country,
                'zip_code':profile.addr_zipcode,
            }})
        return render_to_response('edit_profile.html', context)

@login_required()
def view_profile(request):
    user_account = request.user
    profile = get_object_or_404(UserProfile,user=user_account)
    try:
        bday = str(profile.birthday.year)+'-'+str(profile.birthday.month)+'-'+str(profile.birthday.day);
    except AttributeError:
        bday = ''
    context = RequestContext(request, {'form':{
            'username':user_account,
            'age':profile.get_age(),
            'sex':profile.sex,
            'checked_undefined':"""checked=checked""" if profile.sex == 0 else '',
            'checked_male':"""checked=checked""" if profile.sex == 1 else '',
            'checked_female':"""checked=checked""" if profile.sex == 2 else '',
            'tel':profile.tel,
            'email':profile.user.email,
            'first_name':profile.user.first_name,
            'last_name':profile.user.last_name,
            'birth_date':bday,
            'creditcard':profile.creditcard,
            'first_line':profile.addr_firstline,
            'second_line':profile.addr_secondline,
            'town':profile.addr_town,
            'country':profile.addr_country,
            'zip_code':profile.addr_zipcode,
            }})
    return render_to_response('view_profile.html', context)
