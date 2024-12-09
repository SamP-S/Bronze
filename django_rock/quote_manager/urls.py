from django.urls import path
from .views import quotes_view

urlpatterns = [
    path('', quotes_view)
]
