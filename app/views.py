from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.contrib.auth.decorators import login_required


def home(request):
    all_products = Product.objects.filter(is_available=True)
    
    category_1_products = Product.objects.filter(category__name='Сухие смеси', is_available=True)[:4]
    
    category_2_products = Product.objects.filter(category__name='Готовая еда', is_available=True)[:4]
    
    active_category = request.GET.get('category', 'all')
    
    context = {
        'all_products': all_products,
        'category_1_products': category_1_products,
        'category_2_products': category_2_products,
        'active_category': active_category,
    }
    
    return render(request, 'index.html', context)

def low_calorie_products(request):
    products = Product.get_low_calorie_products(26)
    
    result = ""
    
    for product in products:
        result += f"{product.name} - Калории: {product.calories} ккал\n"
    
    if not result:
        result = "Нет низкокалорийных продуктов"
    
    return HttpResponse(result)



def test(request):
    last_number = request.session.get('last_number')
    
    if request.method == 'POST':
        number_input = request.POST.get('number')
        
        try:
            number = int(number_input)
            request.session['last_number'] = number
            last_number = number
        except:
            pass
    
    return render(request, 'test.html', {'number': last_number})




@login_required
def cart_view(request):
    
    cart_items = Cart.objects.filter(user=request.user)
    
    context = {
        'cart_items': cart_items,
    }
    
    return render(request, 'cart.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    try:
        cart_item = Cart.objects.get(user=request.user, product=product)
        cart_item.quantity += 1
        cart_item.save()
    except Cart.DoesNotExist:
        cart_item = Cart(user=request.user, product=product, quantity=1)
        cart_item.save()
    
    return redirect('home')

@login_required 
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def decrease_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

@login_required
def increase_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    
    if cart_item.quantity >= 1:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')