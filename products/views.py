from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.shortcuts import (
                                render,
                                get_object_or_404,
                                redirect
                             )
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .forms import ProductForm
from .models import Product
from .mixins import AuthRedirectMixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class ProducList(ListView):
    model = Product
# def hello_world(request):
#     # return HttpResponse('<h1>Hello World!</h1>')
#     # return render(request, 'index.html')
#     products = Product.objects.order_by('id')
#     template = loader.get_template('index.html')
#     context = {
#         'products': products,
#     }
#     return HttpResponse(template.render(context, request))

class ProductDetail(AuthRedirectMixin, DetailView):
    model = Product

# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     template = loader.get_template('product_detail.html')
#     context = {
#         'product': product
#     }
#     return HttpResponse(template.render(context, request))

@login_required()
def new_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            product.save()
            return HttpResponseRedirect('/')
    else:
        form = ProductForm()
    template = loader.get_template('new_product.html')
    context = {
        'form': form
    }
    return HttpResponse(template.render(context, request))


def auth_login(request):
    context ={}
    template = loader.get_template('accounts/login.html')
    if request.method == 'POST':
        action = request.POST.get('action', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if action == 'signup':
            repeat_password = request.POST.get('repeat_password', None)
            email = request.POST.get('email', None)
            first_name = request.POST.get('first_name', None)
            last_name = request.POST.get('last_name', None)
            if password == repeat_password:
                user = User.objects.create_user(username = username,
                                                password = password,
                                                email = email,
                                                first_name = first_name,
                                                last_name = last_name)
                try:
                    user.save()
                    user = authenticate(username = username, password=password)
                    login(request,user)
                    return redirect('/')
                except Exception as e:
                    context['signup_invalid']= True
                    context['error_message'] = 'Nombre de usuario ya registrado'
                    return HttpResponse(template.render(context, request))
            else:
                context['password_invalid']= True
                context['error_message'] = 'Las contraseñas no coinciden'
                return HttpResponse(template.render(context, request))
        elif action == 'login':
            user = authenticate(username = username, password=password)
            if user is not None:
                login(request,user)
                next_page = request.GET.get('next', None)
                print(next_page)
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect('/')
            else:
                context['authenticate_invalid']= True
                context['error_message'] = 'Usuario o Contraseña incorrectos'
                return HttpResponse(template.render(context, request))
    context = {}
    return HttpResponse(template.render(context, request))
