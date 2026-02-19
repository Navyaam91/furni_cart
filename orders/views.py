from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.conf import settings

from products.models import Product
from .models import Order, OrderItem
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay
import json

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

# @login_required
# def checkout(request):
#     user = request.user
#     customer = user.customer
#     # Get active cart (order_status = 0)
#     cart = Order.objects.filter(owner=customer, order_status=0).first()

#     if cart:
#         cart.order_status = 1   # mark as checked-out
#         cart.save()

#     return redirect("order_success")   # redirect to success page
@login_required
def checkout(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        owner=request.user.customer,
        order_status=0
    )

    # Prevent duplicate payment
    if order.payment_status == "success":
        return redirect("order_success")

    # Convert to paisa (VERY IMPORTANT)
    amount = int(order.total_price * 100)

    # Initialize Razorpay client
    client = razorpay.Client(auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    ))

    # Create Razorpay Order
    razorpay_order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    # Save details in DB
    order.razorpay_order_id = razorpay_order["id"]
    order.amount = amount
    order.save()

    context = {
        "order": order,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": amount,
    }

    return render(request, "checkout.html", context)
def order_success(request):
    return render(request,'success.html')
@login_required
def orders(request):
    
    user=request.user
    customer=user.customer
    
    all_orders=Order.objects.filter(owner=customer).exclude(order_status=0)
    # print(all_orders)
    #  subtotal = sum(item.total for item in all_orders.cart_items.all()) # cart_items related name from order_item model
    context={'orders':all_orders}
    return render(request,'order.html',context)

@csrf_exempt
def update_cart_quantity(request):
    if request.method == "POST":
        cart_item_id = request.POST.get("cart_item_id")
        quantity = int(request.POST.get("quantity"))

        cart_item = OrderItem.objects.get(id=cart_item_id)
        cart_item.quantity = quantity
        cart_item.save()

        return JsonResponse({
            "success": True,
            "total": cart_item.total
        })
    


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            client = razorpay.Client(auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            ))

            # Verify signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            })

            order = Order.objects.get(
                razorpay_order_id=data['razorpay_order_id']
            )

            order.razorpay_payment_id = data['razorpay_payment_id']
            order.razorpay_signature = data['razorpay_signature']
            order.payment_status = "Success"
            order.order_status = 1  # Confirmed
            order.save()

            return JsonResponse({"status": "success"})

        except Exception as e:
            print("Payment Error:", str(e))
            return JsonResponse({"status": "failed"}, status=400)
