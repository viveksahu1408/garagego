from django.urls import path
from .views import track_call_view

urlpatterns = [
    path('track-call/<int:mechanic_id>/', track_call_view, name='track_call'),
]