from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, Http404
from django.conf import settings
from django.urls import reverse_lazy

from .models import QuoteRequestModel, ProjectModel
from .forms import ProjectForm, QuoteRequestForm

def quotes_view(request):
    return HttpResponse("Hello, World!")

def create_project_and_quote_request(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        quote_request_form = QuoteRequestForm(request.POST)
        
        if project_form.is_valid() and quote_request_form.is_valid():
            project = project_form.save()
            quote_request = quote_request_form.save(commit=False)
            quote_request.project = project
            quote_request.save()
            return redirect("quote_list")
    else:
        project_form = ProjectForm()
        quote_request_form = QuoteRequestForm()
    
    return render(request, 'quote_manager/quote_create.html', {
        'project_form': project_form,
        'quote_request_form': quote_request_form
    })


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

