from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import CallLog
from services.models import MechanicProfile

def track_call_view(request, mechanic_id):
    if request.method == "POST":
        # 1. Mechanic profile ko find karo
        mechanic = get_object_or_404(MechanicProfile, id=mechanic_id)
        
        # 2. Check karo agar user logged in hai, nahi toh None (Anonymous) store hoga
        customer = request.user if request.user.is_authenticated else None
        
        # 3. Call log register karo database me
        CallLog.objects.create(
            customer=customer,
            mechanic=mechanic
        )
        
        return JsonResponse({"status": "success", "message": "Lead tracked successfully!"})
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)