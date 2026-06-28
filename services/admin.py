from django.contrib import admin
from .models import District, ServiceCategory, MechanicProfile
from .models import MechanicServicePrice

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(MechanicProfile)
class MechanicProfileAdmin(admin.ModelAdmin):
    # Admin panel me hi saari details columns me dikhengi
    list_display = ('shop_name', 'user', 'district', 'is_available')
    # Filter karne ka option side me aa jayega district aur availability ke hisab se
    list_filter = ('district', 'is_available')
    search_fields = ('shop_name', 'address')


admin.site.register(MechanicServicePrice)    