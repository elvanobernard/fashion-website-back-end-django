from distutils.command.upload import upload
from tabnanny import verbose
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Category(models.Model):
    category = models.CharField(max_length=50)
    show_in_main = models.BooleanField()
    category_image = models.ImageField(upload_to='category_images', blank=True)
    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category

class Product(models.Model):
    product_code = models.CharField(max_length=10)
    product_name = models.CharField(max_length=50)
    price = models.IntegerField()
    product_desc_short = models.TextField()
    product_desc_long = models.TextField()
    product_information = models.TextField()
    product_photo = models.ImageField(upload_to='product_photo', blank=True)
    categories = models.ManyToManyField(Category)
    trendy = models.BooleanField(default=False)
    new_product = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name


class User(models.Model):
    user_name = models.CharField(max_length=20)
    user_password = models.CharField(max_length=20)
    admin = models.BooleanField()
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    review_text = models.TextField()

class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_photo')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Stock(models.Model):
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=20)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
