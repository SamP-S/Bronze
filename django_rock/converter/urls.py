from django.urls import path
from .views import *

urlpatterns = [
    path('testing/', my_view, name='my_view'),
    path('', my_view, name='conv_home'),
    # quote files
    path('qf/', FCListView.as_view(), name='fc_list'),
    path('qf/create/', FCCreateView.as_view(), name='fc_create'),
    path('qf/<int:pk>/', FCDetailView.as_view(), name='fc_detail'),
    path('qf/<int:pk>/delete/', FCDeleteView.as_view(), name='fc_delete'),
]
