from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout
from django.contrib import messages
from . models import Customer,Contact

def signup(request):
    if request.method == "POST":
        country = request.POST.get("c_country")
        fname = request.POST.get("c_fname")
        lname = request.POST.get("c_lname")
        address = request.POST.get("c_address")
        state = request.POST.get("c_state_country")
        postal_zip = request.POST.get("c_postal_zip")
        email = request.POST.get("c_email_address")
        phone = request.POST.get("c_phone")
        password = request.POST.get("password")
        # email is already registered
        if User.objects.filter(username=email).exists():
            messages.error(request, "User already exists with this email!")
            return redirect('signup')

        # AUTO HASHES PASSWORD
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        Customer.objects.create(
            user=user,
            firstname=fname,
            lastname=lname,
            address=address,
            phone=phone,
            postal_code=postal_zip,
            country=country,
            state=state,
        )

        return redirect('login')

    return render(request, 'signup.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if user exists
        if not User.objects.filter(username=email).exists():
            messages.error(request, "User does not exist!")
            return redirect('login')

        # Authenticate user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('shop')   # change to your dashboard page
        else:
            messages.error(request, "Incorrect password!")
            return redirect('login')

    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('home')
def about(request):
    return render(request, 'about.html')
def contactus(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        message = request.POST.get("message")

        Contact.objects.create(
            first_name=fname,
            last_name=lname,
            email=email,
            message=message
        )

        messages.success(request, "Message sent successfully!")
        return redirect('contactus')

    return render(request, 'contact.html')