from django.shortcuts import render,redirect
from . models import Product, Category, Review
from .forms import ReviewForm
from django.contrib import messages
from customers.models import Customer
from django.core.paginator import Paginator

def index(request):
    product_list=Product.objects.filter(deleted_at=Product.LIVE).order_by('-priority')[:3]
    return render(request, 'index.html',{'product_list':product_list})

def shop(request):
    product_list = Product.objects.filter(deleted_at=Product.LIVE).order_by('-priority')
    categories = Category.objects.all().order_by('-priority')
    
    category_id = request.GET.get('category')
    search_term = request.GET.get('search')
    
    if category_id:
        product_list = product_list.filter(category_id=category_id)
    
    if search_term:
        product_list = product_list.filter(name__icontains=search_term)

    paginator = Paginator(product_list, 8)  # 8 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'shop.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_id,
        'search_term': search_term
    })

def product(request,pk):
    product=Product.objects.get(pk=pk, deleted_at=Product.LIVE)
    reviews = product.reviews.all().order_by('-created_at')
    
    # Calculate average rating
    average_rating = 0
    if reviews.exists():
        total_rating = sum([r.rating for r in reviews])
        average_rating = total_rating / reviews.count()
    
    form = ReviewForm()
    return render(request, 'product.html',{
        'product':product, 
        'reviews': reviews, 
        'form': form,
        'average_rating': average_rating,
        'star_range': range(1, 6)
    })

def add_review(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            try:
                product_obj = Product.objects.get(pk=product_id)
                customer = Customer.objects.get(user=request.user)
                form = ReviewForm(request.POST)
                if form.is_valid():
                    review = form.save(commit=False)
                    review.product = product_obj
                    review.customer = customer
                    review.save()
                    messages.success(request, "Thank you for your review!")
                else:
                    messages.error(request, "There was an error in your review.")
            except (Product.DoesNotExist, Customer.DoesNotExist):
                messages.error(request, "Error adding review.")
            return redirect('product', pk=product_id)
    else:
        messages.error(request, "You must be logged in to add a review.")
        return redirect('login')
    return redirect('home')
