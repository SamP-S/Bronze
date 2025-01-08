from django.urls import path
from .views import *

urlpatterns = [
    path('testing/', my_view, name='my_view'),
    # quote files
    path('', FCListView.as_view(), name='fc_list'),
    path('create/', FCCreateView.as_view(), name='fc_create'),
    path('<int:pk>/', FCDetailView.as_view(), name='fc_detail'),
    path('<int:pk>/delete/', FCDeleteView.as_view(), name='fc_delete'),
]
