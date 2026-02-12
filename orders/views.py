from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Order, OrderItem
from django.contrib import messages


# @login_required
def add_to_cart(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to add items to cart")
        return redirect('login')

    if request.method == "POST":
        # print("ADD TO CART VIEW HIT")
        # print("POST DATA:", request.POST)


        user = request.user
        customer = user.customer

        qty = int(request.POST.get("qty"))
        product_id = request.POST.get("product_id")

        product = Product.objects.get(id=product_id)

        # Cart object
        cart_obj, created = Order.objects.get_or_create(
            owner=customer,
            order_status=0
        )

        # Try to get order item
        order_item, created = OrderItem.objects.get_or_create(
            owner=cart_obj,
            product=product,

        )
        if created:
            order_item.quantity=qty
           
        else:
            order_item.quantity=order_item.quantity+qty

        order_item.save()
        return redirect("cart")


@login_required
def cart(request):
    user = request.user
    customer = user.customer

    cart_obj = Order.objects.filter(
        owner=customer,
        order_status=0
    ).first()
    subtotal = 0
    if cart_obj: 
        subtotal = sum(item.total for item in cart_obj.cart_items.all()) # cart_items related name from order_item model

    context = {
        "cart": cart_obj,        # <- correct variable
        "subtotal": subtotal,
        "total": subtotal
    }

    return render(request, "cart.html", context)
# def checkout(request):
#     return render(request, 'checkout.html')

@login_required
def remove_from_cart(request,pk):
    item=OrderItem.objects.get(pk=pk)
    item.delete()
    return redirect("cart")

@login_required
def checkout(request):
    user = request.user
    customer = user.customer
    # Get active cart (order_status = 0)
    cart = Order.objects.filter(owner=customer, order_status=0).first()

    if cart:
        cart.order_status = 1   # mark as checked-out
        cart.save()

    return redirect("order_success")   # redirect to success page
def order_success(request):
    return render(request,'success.html')
@login_required
def orders(request):
    
    user=request.user
    customer=user.customer
    
    all_orders=Order.objects.filter(owner=customer).exclude(order_status=0)
    # print(all_orders)
    context={'orders':all_orders}
    return render(request,'order.html',context)