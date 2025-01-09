from django.urls import path
from .views import quotes_view, create_project_and_quote_request, QuoteListView, QuoteDetailView

urlpatterns = [
    path('', QuoteListView.as_view(), name="quote_list"),
    path('test', quotes_view),
    path('<int:pk>/', QuoteDetailView.as_view(), name="quote_detail"),
    path('create/', create_project_and_quote_request, name="quote_create"),
]
