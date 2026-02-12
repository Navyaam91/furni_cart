from django.shortcuts import render,redirect
from . models import Product
from django.core.paginator import Paginator
def index(request):
    product_list=Product.objects.order_by('-priority')[:3]
    return render(request, 'index.html',{'product_list':product_list})
def shop(request):
    product_list=Product.objects.all()
    # return render(request, 'shop.html',{'product_list':product_list})
    paginator = Paginator(product_list, 8)  # 8 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop.html', {'page_obj': page_obj})
def product(request,pk):
    product=Product.objects.get(pk=pk)
    return render(request, 'product.html',{'product':product})
