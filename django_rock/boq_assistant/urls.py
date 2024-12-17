from django.urls import path
from .views import *

urlpatterns = [
    path('testing/', my_view, name='my_view'),
    path('', my_view, name='conv_home'),
    # max cut files
    path('mcf/', MCFListView.as_view(), name='mcf_list'),
    path('mcf/create/', MCFCreateView.as_view(), name='mcf_create'),
    path('mcf/<int:pk>/', MCFDetailView.as_view(), name='mcf_detail'),
    path('mcf/<int:pk>/delete/', MCFDeleteView.as_view(), name='mcf_delete'),
    # quote files
    path('qf/', QFListView.as_view(), name='qf_list'),
    path('qf/create/', QFCreateView.as_view(), name='qf_create'),
    path('qf/<int:pk>/', QFDetailView.as_view(), name='qf_detail'),
    path('qf/<int:pk>/delete/', QFDeleteView.as_view(), name='qf_delete'),
]
