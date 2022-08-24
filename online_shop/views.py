import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from .models import Product, Category
from .forms import LogInForm, SignUpForm

# Create your views here.

class IndexView(View):
    def get(self, request):
        categories = Category.objects.filter(show_in_main=True)
        trendy_product = Product.objects.filter(trendy=True)[:8]
        new_product= Product.objects.filter(new_product=True)[:8]



        return render(request, 'online_shop/index.html', {
            'categories': categories,
            'trendy_products': trendy_product,
            'new_product': new_product,
            'user': request.user

        })

class ProductDetailView(View):
    def get(self, request, id):
        product = Product.objects.get(pk=id)
        new_product = Product.objects.filter(new_product=True)[:8]
        return render(request, 'online_shop/product_detail.html', {
            'product': product,
            'products_recommendation': new_product
            })

class ProductsView(View):
    def get(self, request, slug='all'):
        if slug == 'all':
            product = Product.objects.all()
        else:
            product = Category.objects.get(slug=slug).product_set.all()
        return render(request, 'online_shop/shop.html', {
            'products': product
        })

class CartView(View):
    def get(self, request):
        
        context = {}
        
        cart_items = request.session.get('cart_items')
        subtotal = request.session.get('sub_total', 0)
        if cart_items is None or len(cart_items) == 0:
            context['cart_items'] = []
            context['has_items'] = False
        else:
            context['has_items'] = True
            data = Product.objects.filter(id__in=cart_items.keys())
            products = []
            for item in data:
                quantity = cart_items[str(item.id)]
                products.append({
                    'product' : item,
                    'quantity': quantity,
                    'total': item.price * int(quantity)
                    })
            context['products'] = products
        context['subtotal'] = subtotal

        return render(request, 'online_shop/cart.html', context)

    def post(self, request):
        try:
            cart_items = request.session.get('cart_items')
            subtotal = request.session.get('sub_total', 0)
            if cart_items is None:
                cart_items = {}
            
            id = request.POST['product-id']
            quantity = int(request.POST['quantity'])
            price = int(request.POST['price'])
            old_quantity = int(cart_items.get(id, 0))
            action = request.POST['action']
            
            if action == 'add':
                subtotal += (price * quantity)
                quantity += old_quantity
                cart_items[id] = quantity
            elif action == 'mod':
                subtotal += (quantity - old_quantity) * price
                cart_items[id] = quantity
            elif action == 'del':
                subtotal -= (old_quantity) * price
                cart_items.pop(id)


            
            request.session['cart_items'] = cart_items
            request.session['sub_total'] = subtotal

            data = {
                'price': price,
                'quantity': quantity,
                'subtotal': subtotal,
            }
            return HttpResponse(json.dumps(data))
        except:
            return HttpResponse({400})


class CheckOutView(View):
    def get(self, request):
        cart_items = request.session.get('cart_items')
        subtotal = request.session.get('sub_total')
        context = {}
        data = Product.objects.filter(id__in=cart_items.keys())
        products = []
        for item in data:
            quantity = cart_items[str(item.id)]
            products.append({
                'product' : item,
                'quantity': quantity,
                'total': item.price * int(quantity)
            })
        context['products'] = products
        context['subtotal'] = subtotal
        return render(request, 'online_shop/checkout.html', context)
    def post(self, request):
        print(request.POST)
        return HttpResponse('OK')
class ContactView(View):
    def get(self, request):
        print(request.user)
        return render(request, 'online_shop/contact.html')

class LogInView(View):
    def get(self, request):
        login_form = LogInForm()
        return render(request, 'online_shop/authentication.html', {
            'auth_form': login_form,
            'title': 'Log In',
            'action': 'login'
        })

    def post(self, request):
        login_form = LogInForm(request.POST)
        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data.get('email'), password=login_form.cleaned_data.get('password'))
            login(request, user)
            HttpResponseRedirect(reverse('index'))
        return render(request, 'online_shop/authentication.html', {
            'auth_form': login_form,
            'title': 'Log In',
            'action': 'login'
        })

class SignUpView(View):
    def get(self, request):
        signup_form = SignUpForm()
        return render(request, 'online_shop/authentication.html', {
            'auth_form': signup_form,
            'title': 'Sign Up',
            'action': 'signup'
        })
    def post(self, request):
            signup_form = SignUpForm(request.POST)

            if signup_form.is_valid():
                email = signup_form.cleaned_data.get('email')
                password = signup_form.cleaned_data.get('password')
                user = User.objects.create_user(email, email, password)
                user.save()
                return HttpResponseRedirect(reverse('index'))

            return render(request, 'online_shop/authentication.html', {
                'auth_form': signup_form,
                'title': 'Sign Up',
                'action': 'signup'
            })

class LogOutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))