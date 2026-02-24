from .models import Order

def cart_count(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            cart_obj = Order.objects.filter(owner=customer, order_status=0).first()
            if cart_obj:
                # Sum the quantities of all items in the cart
                count = sum(item.quantity for item in cart_obj.cart_items.all())
                return {'cart_count': count}
        except Exception:
            pass
    return {'cart_count': 0}
