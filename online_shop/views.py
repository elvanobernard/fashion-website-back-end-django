from itertools import product
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from .models import Product, Category
from .forms import LogInForm, SignUpForm

dummy_categories = [
    {
        'category': "Men's dresses",
        'image': 'img/cat-1.jpg'
    },
    {
        'category': "Women's dresses",
        'image': 'img/cat-2.jpg'
    },
    {
        'category': "Baby's dresses",
        'image': 'img/cat-3.jpg'
    },
    {
        'category': "Accessories",
        'image': 'img/cat-4.jpg'
    },
    {
        'category': "Bags",
        'image': 'img/cat-5.jpg'
    },
    {
        'category': "Shoes",
        'image': 'img/cat-6.jpg'
    },
]

dummy_products = [
    {   
        'product_name': 'Colorful Stylish Shirt',
        'image': 'img/product-1.jpg',
        'price': '$123.00',
        'discounted-price': '$123.00',
        'id': '511'
    },
    {   
        'product_name': 'Colorful Stylish Shirt',
        'image': 'img/product-2.jpg',
        'price': '$123.00',
        'discounted-price': '$123.00',
        'id': '511'
    },
    {   
        'product_name': 'Colorful Stylish Shirt',
        'image': 'img/product-3.jpg',
        'price': '$123.00',
        'discounted-price': '$123.00',
        'id': '511'
    },
    {   
        'product_name': 'Colorful Stylish Shirt',
        'image': 'img/product-4.jpg',
        'price': '$123.00',
        'discounted-price': '$123.00',
        'id': '511'
    },
    {   
        'product_name': 'Colorful Stylish Shirt',
        'image': 'img/product-5.jpg',
        'price': '$123.00',
        'discounted-price': '$123.00',
        'id': '511'
    },
    {   
        'product_name': 'Colorful Stylish Shirt',
        'image': 'img/product-6.jpg',
        'price': '$123.00',
        'discounted-price': '$123.00',
        'id': '511'
    },
    {   
        'product_name': 'Colorful Stylish Shirt',
        'image': 'img/product-7.jpg',
        'price': '$123.00',
        'discounted-price': '$123.00',
        'id': '511'
    },
    {   
        'product_name': 'Colorful Stylish Shirt',
        'image': 'img/product-8.jpg',
        'price': '$123.00',
        'discounted-price': '$123.00',
        'id': '511'
    },
]

dummy_product_detail = {
    'product_name' : 'Colorful Stylish Shirt',
    'price' : '$150.00',
    'product_desc_short': 'The description doesn’t need to be formal, stick with the language you’re comfortable using on your channels already and remember it should be straightforward and informative rather than overly descriptive. If you’re struggling to write it from your own point of view a trick is to use third person, just like you would with an artist bio.',
    'product_desc_long': """Eos no lorem eirmod diam diam, eos elitr et gubergren diam sea. Consetetur vero aliquyam invidunt duo dolores et duo sit. Vero diam ea vero et dolore rebum, dolor rebum eirmod consetetur invidunt sed sed et, lorem duo et eos elitr, sadipscing kasd ipsum rebum diam. Dolore diam stet rebum sed tempor kasd eirmod. Takimata kasd ipsum accusam sadipscing, eos dolores sit no ut diam consetetur duo justo est, sit sanctus diam tempor aliquyam eirmod nonumy rebum dolor accusam, ipsum kasd eos consetetur at sit rebum, diam kasd invidunt tempor lorem, ipsum lorem elitr sanctus eirmod takimata dolor ea invidunt. Dolore magna est eirmod sanctus dolor, amet diam et eirmod et ipsum. Amet dolore tempor consetetur sed lorem dolor sit lorem tempor. Gubergren amet amet labore sadipscing clita clita diam clita. Sea amet et sed ipsum lorem elitr et, amet et labore voluptua sit rebum. Ea erat sed et diam takimata sed justo. Magna takimata justo et amet magna et.""",
    'product_information': """Eos no lorem eirmod diam diam, eos elitr et gubergren diam sea. Consetetur vero aliquyam invidunt duo dolores et duo sit. Vero diam ea vero et dolore rebum, dolor rebum eirmod consetetur invidunt sed sed et, lorem duo et eos elitr, sadipscing kasd ipsum rebum diam. Dolore diam stet rebum sed tempor kasd eirmod. Takimata kasd ipsum accusam sadipscing, eos dolores sit no ut diam consetetur duo justo est, sit sanctus diam tempor aliquyam eirmod nonumy rebum dolor accusam, ipsum kasd eos consetetur at sit rebum, diam kasd invidunt tempor lorem, ipsum lorem elitr sanctus eirmod takimata dolor ea invidunt.""",
    'image': 'img/product-1.jpg',
    'images': ['img/product-2.jpg', 'img/product-3.jpg', 'img/product-4.jpg'],
    'reviews': [{
        'user_name': 'John',
        'rating': 4,
        'review_text': 'Amazing product.'
    },]
}

# Create your views here.

class IndexView(View):
    def get(self, request):
        categories = Category.objects.filter(show_in_main=True)
        trendy_product = Product.objects.filter(trendy=True)[:8]
        new_product= Product.objects.filter(new_product=True)[:8]

        return render(request, 'online_shop/index.html', {
            'categories': categories,
            'trendy_products': trendy_product,
            'new_product': new_product

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
        return render(request, 'online_shop/contact.html')

class LogInView(View):
    def get(self, request):
        login_form = LogInForm()
        return render(request, 'online_shop/authentication.html', {
            'auth_form': login_form,
            'title': 'Log In'
        })

class SignUpView(View):
    def get(self, request):
        signup_form = SignUpForm()
        return render(request, 'online_shop/authentication.html', {
            'auth_form': signup_form,
            'title': 'Sign Up'
        })