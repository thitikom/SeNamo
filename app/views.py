from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from app.models import *
from django.http import HttpResponse, HttpResponseRedirect
from app.forms import *
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponse("Hello, world. You're at the category index.")

def view_category(request, category_id):
    products_list = Product.objects.filter(category__id = category_id).order_by('name')[:10]
    category_detail = get_object_or_404(Category, id=category_id)
    template = loader.get_template('view_category.html')
    context = Context({
        'products_list': products_list,
        'category_detail': category_detail,
        })
    return HttpResponse(template.render(context))
    #    return HttpResponse("You're looking at category %s." % category_id)

def view_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render_to_response('view_product.html', {'product': product},
        context_instance=RequestContext(request,{
            'messages': messages}))

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
    context = RequestContext(request, { 'form': add_product_form() })

    if request.method == 'POST':
        anpf = add_product_form(request.POST, request.FILES)
        data = anpf.data

        if anpf.is_valid():
            data = anpf.cleaned_data

            # file type validation
            file_type = data['image'].content_type.split('/')[0]
            if file_type != 'image':
                context = update_product_context(context, data, 'file_type_error', 'image file only!')
                return render_to_response('add_product.html', context)

            # create obj
            product = Product.objects.get_or_create(name=data['name'], price=data['price'], point=data['point'],
                category=data['category'], description=data['description'],image=request.FILES['image'])[0]
            product.save()
            context.update(
                    {'form': add_product_form, 'success': 'product created successfully'}
            )
            return render_to_response('add_product.html', context)
        else:
            context = update_product_context(context, data, 'form_error', 'please fill all required informations')
            return render_to_response('add_product.html', context)
    else:
        return render_to_response('add_product.html', context)

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = RequestContext(request, {'form': add_product_form()})

    if request.method == 'GET':
        context = RequestContext(request, {
            'form': add_product_form(
                initial={'name': product.name, 'price': product.price, 'point': product.point,
                         'category': product.category, 'description': product.description,
                         'image': product.image}
            ),
            'product': product,
            'cid': product.id
        })
        return render_to_response('edit_product.html', context)
    else:
        apf = add_product_form(request.POST, request.FILES, instance=product)
        #data = apf.data
        if apf.is_valid():
            apf.save()
        else:
            apf = add_product_form(instance=product)

        return HttpResponseRedirect('/product/%d' % product.id)

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
                    {'form': add_category_form, 'success_msg': 'category created successfully'}
            )
            return render_to_response('add_category.html', context)
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
            return HttpResponseRedirect('/category/%d' % category.id)
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
    return render_to_response('delete_product.html',context)

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()

    messages.add_message(request, messages.SUCCESS, 'Successfully delete category.')
    context = RequestContext(request, {
        messages : messages
    })
    return render_to_response('delete_product.html', context)

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
    (total_price,total_point) = calc_price_point(request)
    context = RequestContext(request, {'product_in_cart': request.session['product_in_cart'],
                                       'total_price':total_price,
                                       'total_point':total_point})
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

    return render_to_response('view_order_detail.html',
            {
                'order': order,
                'products_list': list,
                'total_price': total_price,
                'total_point': total_point,
            })

#Checkout

@login_required
def checkout_payment(request):
    user = request.user
    if request.method == 'GET':
        user_profile = user.get_profile()
        (total_price,total_point) = calc_price_point(request)
        context = RequestContext(request, {'form': credit_card_form(),
                                           'oldcard': user_profile.creditcard,
                                           'total_price': total_price,
                                           'total_point': total_point,
                                           })
        return render_to_response('checkout_payment.html',context)
    else: #POST
        #request.POST.get('select_card')
        return HttpResponse("OK GOOD")

@login_required(redirect_field_name='/cart')
def checkout_shipping(request):
    user = request.user
    if request.method == 'GET':
        user_profile = user.get_profile()
        (total_price,total_point) = calc_price_point(request)
        context = RequestContext(request, {'form': address_form(),
                                           'oldaddress': user_profile.get_address(),
                                           'total_price': total_price,
                                           'total_point': total_point,
                                           })
        return render_to_response('checkout_shipping.html',context)

def checkout_finish(request):
    pass

def checkout_problem(request):
    pass

def view_order_history(request):
    user_account = request.user
    order_list = Order.objects.filter(user=user_account).order_by('timestamp')
    context = Context({
        'order_list':order_list,
        'messages':messages
    })
    return render_to_response('view_order_history.html',context)
