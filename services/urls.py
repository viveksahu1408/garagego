from django.urls import path
from .views import (
    home_view, 
    mechanic_register_view, 
    mechanic_login_view, 
    mechanic_dashboard_view, 
    mechanic_logout_view
)

from .views import owner_dashboard_view

urlpatterns = [
    path('', home_view, name='home'),
    path('join-mechanic/', mechanic_register_view, name='mechanic_register'),
    path('mechanic/login/', mechanic_login_view, name='mechanic_login'),
    path('mechanic/dashboard/', mechanic_dashboard_view, name='mechanic_dashboard'),
    path('mechanic/logout/', mechanic_logout_view, name='mechanic_logout'),
    path('owner/dashboard/', owner_dashboard_view, name='owner_dashboard'), # Ye line jodo
 
 ]