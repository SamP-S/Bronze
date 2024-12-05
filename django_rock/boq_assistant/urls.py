from django.urls import path
from .views import MyView, MCFCreateView, MCFListView, MCFDetailView, MCFUpdateView, MCFDeleteView

urlpatterns = [
    path('testing/', MyView.as_view(), name='my_view'),
    path('', MCFListView.as_view(), name='mcf_list'),
    path('create/', MCFCreateView.as_view(), name='mcf_create'),
    path('tasks/<int:pk>/', MCFDetailView.as_view(), name='mcf_detail'),
    path('tasks/<int:pk>/update/', MCFUpdateView.as_view(), name='mcf_update'),
    path('tasks/<int:pk>/delete/', MCFDeleteView.as_view(), name='mcf_delete'),
]
