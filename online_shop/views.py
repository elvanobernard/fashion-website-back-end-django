import imp
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from .models import Product, Category
from .forms import LogInForm, SignUpForm


class IndexView(View):
    def get(self, request):
        # Query for products & categories that will be shown on main page
        categories = Category.objects.filter(show_in_main=True)
        trendy_product = Product.objects.filter(trendy=True)[:8]
        new_product= Product.objects.filter(new_product=True)[:8]

        return render(request, 'online_shop/index.html', {
            'categories': categories,
            'trendy_products': trendy_product,
            'new_product': new_product,

        })


class ProductDetailView(View):
    def get(self, request, id):
        # Query product based on id and return the detail
        product = Product.objects.get(pk=id)
        new_product = Product.objects.filter(new_product=True)[:8]
        return render(request, 'online_shop/product_detail.html', {
            'product': product,
            'products_recommendation': new_product,
            })


def retrieve_products(slug:str) -> Product:
    """
        Function to retrieve all products from database with / without category.

        :param slug: The string that will be used to query for specific category products
        :return: QuerySet of Product model
    """
    if slug == 'all':
        product = Product.objects.all()
    else:
        try:
            product = Category.objects.get(slug=slug).product_set.all()
        except:
            product = []
    return product


class ProductsView(View):
    def get(self, request, slug='all'):
        product = retrieve_products(slug)

        return render(request, 'online_shop/shop.html', {
            'products': product,
        })

    def post(self, request, slug='all'):
        product = []
        
        # Check if filters exist in request
        if request.POST.get('filter'):
            
            # Transform filters in request into array
            filters = map(int, request.POST.get('filter').split(','))

            q_objects = Q()

            # Creating and appending new Q objects based on filters
            for filter in filters:
                q_objects |= Q(price__range=(filter*100 - 100, filter*100))

            # Perform query using filter
            if slug == 'all':
                product = Product.objects.filter(q_objects)
            else:
                try:
                    product = Category.objects.get(slug=slug).product_set.filter(q_objects)
                except:
                    product = []
            
        # Query for all product if filters not found
        else:
            product = retrieve_products(slug)

        # Return products template / "no product" template based on checking of product variable
        template = 'online_shop/'
        if product:
            template += 'filtered_shop_products.html'
        else:
            template += 'no_products.html'

        return render(request, template, {
            'products': product,
        })


class CartView(View):
    def get(self, request):
        context = {}
        cart_items = request.session.get('cart_items')
        subtotal = request.session.get('sub_total', 0)

        # Create new empty cart items if none exist in session
        if cart_items is None or len(cart_items) == 0:
            context['cart_items'] = {}
            context['has_items'] = False

        # Query for products from database if cart items contain item
        else:
            context['has_items'] = True
            data = Product.objects.filter(id__in=cart_items.keys())

            # Create an array of products that will be rendered in template
            products = []
            for item in data:
                quantity = cart_items[str(item.id)]
                products.append({
                    'product' : item,
                    'quantity': quantity,
                    'total': item.price * int(quantity),
                    })
            context['products'] = products

        # Add subtotal into the context that will be passed into template
        context['subtotal'] = subtotal

        return render(request, 'online_shop/cart.html', context)

    def post(self, request):
        try:
            # Retrieve existing cart items and subtotal from session
            cart_items = request.session.get('cart_items')
            subtotal = request.session.get('sub_total', 0)
            
            # Create empty cart items if none exist in session
            if cart_items is None:
                cart_items = {}
            
            # Obtain the id, quantity, and price per unit of product added to cart items from request
            id = request.POST['product-id']
            quantity = int(request.POST['quantity'])
            price = int(request.POST['price'])

            # Obtain the existing quantity (if any) from cart items
            old_quantity = int(cart_items.get(id, 0))

            # Obtain the action to perform from request
            action = request.POST['action']
            
            # 'add' action comes from product detail page
            if action == 'add':
                subtotal += (price * quantity)
                quantity += old_quantity
                cart_items[id] = quantity

            # 'mod' action comes from cart page
            elif action == 'mod':
                subtotal += (quantity - old_quantity) * price
                cart_items[id] = quantity

            # 'del' action comes from cart page
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
        # Obtain the cart items and subtotal from session
        cart_items = request.session.get('cart_items')
        subtotal = request.session.get('sub_total')
        context = {}

        # If cart items not empty, obtain the product from database
        if cart_items:
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
        # Will be implemented later
        return HttpResponse('OK')


class ContactView(View):
    def get(self, request):
        # Will be implemented later
        return render(request, 'online_shop/contact.html')


class LogInView(View):
    def get(self, request):
        # Create login form and render the template
        login_form = LogInForm()
        return render(request, 'online_shop/authentication.html', {
            'auth_form': login_form,
            'title': 'Log In',
            'action': 'login',
        })

    def post(self, request):

        # Obtain and authenticate user
        login_form = LogInForm(request.POST)
        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data.get('email'), password=login_form.cleaned_data.get('password'))
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                login_form.add_error(None, ValidationError("Incorrect username or password", code='invalid_credential'))
        
        return render(request, 'online_shop/authentication.html', {
            'auth_form': login_form,
            'title': 'Log In',
            'action': 'login',
        })


class SignUpView(View):
    def get(self, request):
        # Create signup form and render the template
        signup_form = SignUpForm()
        return render(request, 'online_shop/authentication.html', {
            'auth_form': signup_form,
            'title': 'Sign Up',
            'action': 'signup',
        })

    def post(self, request):
            # Obtain form data
            signup_form = SignUpForm(request.POST)

            # Perform validation and save user if valid
            if signup_form.is_valid():
                email = signup_form.cleaned_data.get('email')
                password = signup_form.cleaned_data.get('password')
                user = User.objects.create_user(email, email, password)
                user.save()
                return HttpResponseRedirect(reverse('index'))

            return render(request, 'online_shop/authentication.html', {
                'auth_form': signup_form,
                'title': 'Sign Up',
                'action': 'signup',
            })


class LogOutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))
