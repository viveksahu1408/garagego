from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CarListing
from services.models import District
from django.contrib.auth.decorators import user_passes_test


# 1. Car Sell karne ka Form View
#@login_required(login_url='mechanic_login')
def sell_car_view(request):
    cities = District.objects.all()
    message = None

    if request.method == "POST":
        # Check karenge ki user logged in hai ya anonymous (public)
        current_seller = request.user if request.user.is_authenticated else None

        CarListing.objects.create(
            seller=current_seller, # 👈 Ab bina login ke bhi crash nahi hoga, None chala jayega
            seller_name=request.POST.get('seller_name'),
            seller_phone=request.POST.get('seller_phone'),
            
            # Specs
            brand=request.POST.get('brand'),
            car_name=request.POST.get('car_name'),
            model_year=request.POST.get('model_year'),
            kms_driven=request.POST.get('kms_driven'),
            fuel_type=request.POST.get('fuel_type'),
            condition=request.POST.get('condition'),
            expected_price=request.POST.get('expected_price'),
            city_id=request.POST.get('city'),
            description=request.POST.get('description'),
            
            # Docs
            insurance_status=request.POST.get('insurance_status'),
            has_rc_card=True if request.POST.get('has_rc_card') else False,
            has_noc=True if request.POST.get('has_noc') else False,
            
            # 4 Photos Capture
            image_front=request.FILES.get('image_front'),
            image_back=request.FILES.get('image_back'),
            image_interior=request.FILES.get('image_interior'),
            image_dashboard=request.FILES.get('image_dashboard')
        )
        message = "Aapki gadi ki complete details aur photos verification ke liye bhej di gayi hain!"

    return render(request, 'car_bazaar/sell_car.html', {'cities': cities, 'message': message})


# 2. Car Bazaar Public Marketplace View (With City Filter)
def car_marketplace_view(request):
    cities = District.objects.all()
    selected_city = request.GET.get('city')
    
    # Sirf wahi gaadiyan dikhao jo Approved hain
    listings = CarListing.objects.filter(is_approved=True).select_related('city')
    
    # City filter logic
    if selected_city:
        listings = listings.filter(city_id=selected_city)
        
    # Owner ka main support call number jahan user contact karega commission bachaane ke liye
    # (Yahan aap apna ya client ka actual support call number set kar sakte hain)
    owner_support_number = "9876543210" 

    context = {
        'cities': cities,
        'listings': listings,
        'selected_city': selected_city,
        'owner_support_number': owner_support_number
    }
    return render(request, 'car_bazaar/marketplace.html', context)


def is_owner(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_owner, login_url='mechanic_login')
def owner_car_detail_view(request, car_id):
    car = get_object_or_404(CarListing, id=car_id)
    
    if request.method == "POST":
        action = request.POST.get('action')
        
        if action == "update_and_approve":
            # Pricing aur Description update
            car.expected_price = request.POST.get('expected_price')
            car.description = request.POST.get('description')
            
            # Agar owner ne kisi angle ki photo replace ki ho
            if request.FILES.get('image_front'): car.image_front = request.FILES.get('image_front')
            if request.FILES.get('image_back'): car.image_back = request.FILES.get('image_back')
            if request.FILES.get('image_interior'): car.image_interior = request.FILES.get('image_interior')
            if request.FILES.get('image_dashboard'): car.image_dashboard = request.FILES.get('image_dashboard')
            
            # Direct approve kar do yahan se
            car.is_approved = True
            car.save()
            return redirect('owner_dashboard')
            
        elif action == "reject_delete":
            car.delete()
            return redirect('owner_dashboard')

    return render(request, 'car_bazaar/owner_car_detail.html', {'car': car})