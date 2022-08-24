from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('products', views.ProductsView.as_view()),
    path('products/<int:id>', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<slug:slug>', views.ProductsView.as_view(), name = 'category-product'),
    path('cart', views.CartView.as_view(), name='cart'),
    path('checkout', views.CheckOutView.as_view(), name='checkout'),
    path('contact-us', views.ContactView.as_view()),
    path('login', views.LogInView.as_view(), name='login'),
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('logout', views.LogOutView.as_view(), name='logout'),
]