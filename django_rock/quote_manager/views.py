from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, Http404
from django.conf import settings
from django.urls import reverse_lazy
from .models import QuoteRequestModel, ProjectModel

def quotes_view(request):
    return HttpResponse("Hello, World!")

class QuoteListView(ListView):
    model = QuoteRequestModel
    template_name = "quote_manager/quote_list.html"
    context_object_name = "quote_list"

class QuoteDetailView(DetailView):
    model = QuoteRequestModel
    template_name = "quote_manager/quote_detail.html"
    context_object_name = "quote"
    
class QuoteCreateView(CreateView):
    model = QuoteRequestModel
    template_name = "quote_manager/quote_create.html"
    fields = [
        "project",
        "company",
        "contact_name",
        "contact_email",
        "date_in",
        "contact_phone",
        "date_close",
        "date_sent",
    ]
    success_url = reverse_lazy("quote_manager:quote_list")
    
class QuoteUpdateView(UpdateView):
    model = QuoteRequestModel
    template_name = "quote_manager/quote_update.html"
    fields = [
        "project",
        "company",
        "contact_name",
        "contact_email",
        "date_in",
        "contact_phone",
        "date_close",
        "date_sent",
    ]
    
class QuoteDeleteView(DeleteView):
    model = QuoteRequestModel
    template_name = "quote_manager/quote_delete.html"
    success_url = reverse_lazy("quote_manager:quote_list")

