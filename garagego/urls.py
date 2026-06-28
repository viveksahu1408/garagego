from django.contrib import admin
from django.urls import path, include # 'include' add karo
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('services.urls')), # Main domain par hi hamara home page khulega
    path('leads/', include('leads_experts.urls')),
    path('bazaar/', include('car_bazaar.urls')),

]


# Aapke saare url paths ke baad check karo:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)