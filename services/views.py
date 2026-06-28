from django.shortcuts import render
from .models import District, ServiceCategory, MechanicProfile,MechanicServicePrice
from accounts.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import MechanicProfile, MechanicServicePrice, ServiceCategory
from django.contrib.auth.decorators import user_passes_test
from leads_experts.models import CallLog
from car_bazaar.models import CarListing


def home_view(request):
    districts = District.objects.all()
    categories = ServiceCategory.objects.all()
    
    selected_district = request.GET.get('district')
    selected_category = request.GET.get('category')
    
    # Starting query with prefetch_related for better performance
    mechanics = MechanicProfile.objects.filter(is_available=True).prefetch_related('mechanicserviceprice_set__service')
    
    if selected_district:
        mechanics = mechanics.filter(district_id=selected_district)
        
    if selected_category:
        mechanics = mechanics.filter(services_offered__id=selected_category)
        
    context = {
        'districts': districts,
        'categories': categories,
        'mechanics': mechanics,
        'selected_district': selected_district,
        'selected_category': selected_category,
    }
    return render(request, 'services/home.html', context)

def mechanic_register_view(request):
    districts = District.objects.all()
    categories = ServiceCategory.objects.all() # Form me dikhane ke liye saari services nikal lo
    success_message = None

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        shop_name = request.POST.get('shop_name')
        district_id = request.POST.get('district')
        address = request.POST.get('address')

        # 1. User Create Karo
        user = User.objects.create_user(username=username, password=password)
        user.is_mechanic = True
        user.phone_number = phone_number
        user.save()

        # 2. Mechanic Profile Create Karo
        mechanic_profile = MechanicProfile.objects.create(
            user=user,
            shop_name=shop_name,
            district_id=district_id,
            address=address,
            is_available=False # Approval pending
        )
        
        # 3. Dynamic Services aur Pricing Save Karo
        for category in categories:
            # Check karo ki kya is category ka checkbox tick kiya hai
            is_selected = request.POST.get(f'service_{category.id}')
            if is_selected:
                # Us category ka price nikal lo, agar khali choda toh 0.00 default
                price_val = request.POST.get(f'price_{category.id}', 0)
                if not price_val:
                    price_val = 0
                
                # Intermediary table me save karo
                MechanicServicePrice.objects.create(
                    mechanic=mechanic_profile,
                    service=category,
                    base_price=price_val
                )
        
        success_message = "Aapki profile aur services successfully register ho gayi hain! Jald hi live hogi."

    return render(request, 'services/mechanic_register.html', {
        'districts': districts,
        'categories': categories,
        'success_message': success_message
    })


# 1. Mechanic Login View
def mechanic_login_view(request):
    error_msg = None
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        
        if user is not None and user.is_mechanic:
            login(request, user)
            return redirect('mechanic_dashboard')
        else:
            error_msg = "Sahi details dalein ya approval ka wait karein!"

    return render(request, 'services/mechanic_login.html', {'error_msg': error_msg})

# 2. Protected Dashboard View (Sirf Logged-in Mechanics ke liye)
@login_required(login_url='mechanic_login')
def mechanic_dashboard_view(request):
    # Logged-in user ki profile nikalo
    mechanic = get_object_or_404(MechanicProfile, user=request.user)
    
    if request.method == "POST":
        action = request.POST.get('action')
        
        # Action 1: Status toggle (Online/Offline)
        if action == "toggle_status":
            mechanic.is_available = not mechanic.is_available
            mechanic.save()
            
        # Action 2: Price update logic
        elif action == "update_prices":
            for sp in mechanic.mechanicserviceprice_set.all():
                new_price = request.POST.get(f'price_{sp.id}')
                if new_price:
                    sp.base_price = new_price
                    sp.save()
            return redirect('mechanic_dashboard')

    # Dashboard par analytics metrics (jaise kitne call aaye background me lead_experts se)
    total_calls = mechanic.calllog_set.count() # Lead count
    
    context = {
        'mechanic': mechanic,
        'total_calls': total_calls,
    }
    return render(request, 'services/mechanic_dashboard.html', context)

# 3. Logout View
def mechanic_logout_view(request):
    logout(request)
    return redirect('mechanic_login')


# Check karega ki kya login banda staff/superuser hai
def is_owner(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_owner, login_url='mechanic_login')
def owner_dashboard_view(request):
    total_mechanics = MechanicProfile.objects.count()
    active_mechanics = MechanicProfile.objects.filter(is_available=True).count()
    total_leads = CallLog.objects.count()
    pending_mechanics = MechanicProfile.objects.filter(user__is_mechanic=True, is_available=False)
    all_mechanics = MechanicProfile.objects.all().prefetch_related('calllog_set')
    
    # --- YEH NAYA CODE HAI CAR BAZAAR VERIFICATION KE LIYE ---

# Context me existing pending_cars ke sath approved_cars bhi bhejo
    pending_cars = CarListing.objects.filter(is_approved=False).select_related('city')
    approved_cars = CarListing.objects.filter(is_approved=True).select_related('city') # 👈 Naya filter

    if request.method == "POST":
        action = request.POST.get('action')
        
        if action == "approve":
            mech_id = request.POST.get('mechanic_id')
            mech = get_object_or_404(MechanicProfile, id=mech_id)
            mech.is_available = True
            mech.save()
            return redirect('owner_dashboard')
            
        # Naya Action: Car Listing Verification Approval
        elif action == "approve_car":
            car_id = request.POST.get('car_id')
            car = get_object_or_404(CarListing, id=car_id)
            car.is_approved = True
            car.save()
            return redirect('owner_dashboard')
        
    # Owner dwara car ki details update karne ya image replace karne ka logic
        elif action == "update_car_details":
            car_id = request.POST.get('car_id')
            car = get_object_or_404(CarListing, id=car_id)
            
            # Owner can override pricing or description if watermarks/numbers are found
            car.expected_price = request.POST.get('expected_price')
            car.description = request.POST.get('description')
            
            # Agar owner ne nayi image select ki hai toh replace kar do
            if request.FILES.get('new_car_image'):
                car.car_image = request.FILES.get('new_car_image')
                
            car.save()
            return redirect('owner_dashboard')
    # --------------------------------------------------------

    context = {
        'total_mechanics': total_mechanics,
        'active_mechanics': active_mechanics,
        'total_leads': total_leads,
        'pending_mechanics': pending_mechanics,
        'all_mechanics': all_mechanics,
        'pending_cars': pending_cars, # Car list context me bheja
        'approved_cars': approved_cars, # 👈 Context me pass kiya
    }
    return render(request, 'services/owner_dashboard.html', context)