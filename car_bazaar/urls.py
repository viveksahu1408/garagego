from django.urls import path
from .views import sell_car_view, car_marketplace_view,owner_car_detail_view

app_name = 'car_bazaar'

urlpatterns = [
    path('marketplace/', car_marketplace_view, name='car_marketplace'),
    path('marketplace/sell/', sell_car_view, name='sell_car'),
    path('owner/car/<int:car_id>/', owner_car_detail_view, name='owner_car_detail'), # 👈 Naya route
]