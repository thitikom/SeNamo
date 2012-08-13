from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from app.models import Product, Category
from django.http import HttpResponse, HttpResponseRedirect
from app.forms import add_product_form, add_category_form

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
    return render_to_response('view_product.html', {'product': product})

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
        apf = add_product_form(request.POST)
        data = apf.data

        if apf.is_valid():
            data = apf.cleaned_data

            if data['image'] is not None:
                # file type validation
                file_type = data['image'].content_type.split('/')[0]
                if file_type != 'image':
                    context = update_product_context(context, data, 'file_type_error', 'image file only!')
                    return render_to_response('edit_product.html', context)

            product.name = data['name']
            product.price = data['price']
            product.point = data['point']
            product.category = data['category']
            product.description = data['description']
            if request.FILES['image'] is not None:
                product.image = request.FILES['image']
            product.save()
            return HttpResponseRedirect('/product/%d' % product.id)
        else:
            context = update_product_context(context, data, 'form_error', 'please fill all required informations')
            return render_to_response('edit_product.html', context)

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