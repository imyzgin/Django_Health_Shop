from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('calorie/', views.low_calorie_products, name='low_calorie_products'),
    path('test/', views.test, name = 'test'),
    # path('diet/<str:diet_name>/', views.products_by_diet, name='products_by_diet'),
    # path('brand/<str:brand_name>/', views.products_by_brand, name='products_by_brand'), 
    # # path('category/<int:category_id>/', views.products_by_category, name='products_by_category'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/increase/<int:cart_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:cart_id>/', views.decrease_quantity, name='decrease_quantity'),

]