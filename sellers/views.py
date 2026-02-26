from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from customers.models import Customer
from products.models import Product, Category
from orders.models import Order, OrderItem
from django.contrib import messages

def is_seller_check(user):
    return hasattr(user, 'customer') and user.customer.is_seller

@login_required
def become_seller(request):
    if hasattr(request.user, 'customer'):
        customer = request.user.customer
        customer.is_seller = True
        customer.save()
        messages.success(request, "Congratulations! You are now a seller.")
        return redirect('seller_dashboard')
    messages.error(request, "Customer profile not found.")
    return redirect('shop')

@login_required
def dashboard(request):
    if not is_seller_check(request.user):
        messages.error(request, "You are not a registered seller.")
        return redirect('shop')
    
    customer = request.user.customer
    products = Product.objects.filter(seller=customer)
    total_products = products.count()
    
    # Simple order fetching for items belonging to this seller
    order_items = OrderItem.objects.filter(product__seller=customer).exclude(owner__order_status=0)
    total_orders = order_items.values('owner').distinct().count()
    
    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'recent_products': products.order_by('-created_at')[:5],
    }
    return render(request, 'sellers/dashboard.html', context)

@login_required
def product_list(request):
    if not is_seller_check(request.user):
        return redirect('shop')
    
    products = Product.objects.filter(seller=request.user.customer).order_by('-created_at')
    return render(request, 'sellers/product_manage.html', {'products': products})

@login_required
def add_product(request):
    if not is_seller_check(request.user):
        return redirect('shop')
    
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')
        
        category = Category.objects.get(id=category_id)
        
        Product.objects.create(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category=category,
            image=image,
            seller=request.user.customer,
            deleted_at=1 # Live
        )
        messages.success(request, "Product added successfully!")
        return redirect('seller_product_list')
    
    categories = Category.objects.all()
    return render(request, 'sellers/add_product.html', {'categories': categories})

@login_required
def update_stock(request, pk):
    if not is_seller_check(request.user):
        return redirect('shop')
    
    product = get_object_or_404(Product, pk=pk, seller=request.user.customer)
    if request.method == "POST":
        stock = request.POST.get('stock')
        product.stock = stock
        product.save()
        messages.success(request, f"Stock for {product.name} updated!")
    return redirect('seller_product_list')

@login_required
def order_list(request):
    if not is_seller_check(request.user):
        return redirect('shop')
    
    # Get all order items for products owned by this seller
    order_items = OrderItem.objects.filter(product__seller=request.user.customer).exclude(owner__order_status=0).order_by('-created_at')
    return render(request, 'sellers/order_manage.html', {'order_items': order_items})

@login_required
def update_order_status(request, pk):
    if not is_seller_check(request.user):
        return redirect('shop')
    
    # In a simple system, we might update the whole order or just the item
    # Let's say the seller can "Process" their part of the order
    order_item = get_object_or_404(OrderItem, pk=pk, product__seller=request.user.customer)
    # For now, let's just show status on the order itself if needed, or item status
    # Order model has ORDER_STATUS_CHOICES: (1, 'Confirmed'), (2, 'Processed'), (3, 'Delivered')
    if request.method == "POST":
        new_status = request.POST.get('status')
        order = order_item.owner
        order.order_status = new_status
        order.save()
        messages.success(request, "Order status updated!")
    return redirect('seller_order_list')

@login_required
def payment_list(request):
    if not is_seller_check(request.user):
        return redirect('shop')
    
    # Filter orders that have seller's products and are paid
    orders = Order.objects.filter(cart_items__product__seller=request.user.customer, payment_status='success').distinct()
    
    # Add amount in rupees for each order
    for order in orders:
        order.amount_in_rupees = order.amount / 100.0
        
    return render(request, 'sellers/payment_list.html', {'orders': orders})
