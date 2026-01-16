from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
# from django.contrib.auth.models import User
from django.conf import settings 

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name


class Diet(models.Model):
    
    DIET_TYPES = [
        ('sugar_free', 'Без сахара'),
        ('vegan', 'Для веганов'),
        ('vegetarian', 'Для вегетарианцев'),
        ('lactose_free', 'Без лактозы'),
        ('gluten_free', 'Без глютена'),
    ]
    
    name = models.CharField(max_length=20, choices=DIET_TYPES, unique=True)
    description = models.TextField(blank=True, help_text="Краткое описание диеты")
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    diets = models.ManyToManyField(Diet, blank=True) 
    description = models.TextField()
    calories = models.IntegerField()  
    protein = models.DecimalField(max_digits=5, decimal_places=1)
    fats = models.DecimalField(max_digits=5, decimal_places=1)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=1)  
    brand = models.CharField(max_length=100)
    price = models.DecimalField(default=0.01, max_digits=10, decimal_places=2, 
                               validators=[MinValueValidator(Decimal('0.01'))])
    unit_choices = [
        ('шт', 'Штуки'),
        ('кг', 'Килограммы'),
        ('г', 'Граммы'),
        ('л', 'Литр'),
        ('мл', 'Миллилитры'),
    ]
    unit = models.CharField(max_length=10, choices=unit_choices, default='шт')
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    image = models.ImageField(upload_to="product_images/", blank=True)
    
    def __str__(self):
        return f"{self.name}"
    
    
    def get_low_calorie_products(max_calories):
        return Product.objects.filter(calories__lte=max_calories,is_available=True).order_by('calories')
    
    def get_high_protein_products(min_protein):
        return Product.objects.filter(protein__gte=min_protein,is_available=True).order_by('-protein')
    
    def get_products_for_diet(diet_name):
        return Product.objects.filter(diets__name=diet_name,is_available=True).order_by('name')
    
    
    
    
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    RATING_CHOICES = [
        (1, '1 - Очень плохо'),
        (2, '2 - Плохо'),
        (3, '3 - Нормально'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    ]

    rating = models.IntegerField(choices=RATING_CHOICES)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Отзыв от {self.user.username}"
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ('user', 'product')  
    def __str__(self):
        return f"{self.quantity} x {self.product.name} в корзине {self.user.username}"
    
    def get_total_price(self):
        return self.quantity * self.product.price