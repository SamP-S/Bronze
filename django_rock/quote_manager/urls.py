from django.urls import path
from .views import *

urlpatterns = [
    path('', QuoteListView.as_view(), name="quote_list"),
    path('test', quotes_view),
    path('<int:pk>/', QuoteDetailView.as_view(), name="quote_detail"),
    path('create/', create_project_and_quote_request, name="quote_create"),
    path('<int:pk>/update', QuoteUpdateView.as_view(), name="quote_update"),
    path('<int:pk>/delete', QuoteDeleteView.as_view(), name="quote_delete"),
    
    # backlog
    path('backlog/', BacklogListView.as_view(), name="quote_backlog"),
]
