from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, Http404
from django.conf import settings
from django.urls import reverse_lazy

from .models import QuoteModel, ProjectModel, ProjectBlacklist, CompanyBlacklist
from .forms import ProjectForm, QuoteForm

# TODO: convert all url redirects to use correct look up namespacing e.g. my_app:my_view
# for redirect, reverse, reverse_lazy

def quotes_view(request):
    return HttpResponse("Hello, World!")
    
def create_project_and_quote_request(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        quote_form = QuoteForm(request.POST)
        
        if quote_form.is_valid() and project_form.is_valid():
            if project_form.is_valid():
                project = project_form.save()
                quote_request = quote_form.save(commit=False)
                quote_request.project = project
                quote_request.save()
            return redirect("quote_list")
    else:
        project_form = ProjectForm()
        quote_form = QuoteForm()
    
    return render(request, 'quote_manager/quote_create.html', {
        'project_list': ProjectModel.objects.all().order_by('address'),
        'project_form': project_form,
        'quote_form': quote_form
    })
        

class BacklogListView(ListView):
    model = QuoteModel
    template_name = "quote_manager/quote_list.html"
    context_object_name = "quote_list"
    
    def get_queryset(self):
        return super().get_queryset().filter(project__estimater__isnull=True)
    

class QuoteListView(ListView):
    model = QuoteModel
    template_name = "quote_manager/quote_list.html"
    context_object_name = "quote_list"

class QuoteDetailView(DetailView):
    model = QuoteModel
    template_name = "quote_manager/quote_detail.html"
    context_object_name = "quote"
    
class QuoteCreateView(CreateView):
    model = QuoteModel
    template_name = "quote_manager/quote_create.html"
    fields = ["project", "company", "contact_name", "contact_email", "date_in", "contact_phone", "date_close", "date_sent",
    ]
    success_url = reverse_lazy("quote_manager:quote_list")
    
class QuoteUpdateView(UpdateView):
    model = QuoteModel
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
    model = QuoteModel
    template_name = "quote_manager/quote_delete.html"
    success_url = reverse_lazy("quote_manager:quote_list")



##### PROJECT BLACKLIST #####
class ProjectBlacklistListView(ListView):
    model = ProjectBlacklist
    template_name = "quote_manager/project_blacklist_list.html"
    context_object_name = "blacklist_project_list"
    
class ProjectBlacklistDetailView(DetailView):
    model = ProjectBlacklist
    template_name = "quote_manager/project_blacklist_detail.html"
    context_object_name = "blacklist_project"

class ProjectBlacklistCreateView(CreateView):
    model = ProjectBlacklist
    template_name = "quote_manager/project_blacklist_create.html"
    fields = [
        "project",
        "reason",
    ]
    success_url = reverse_lazy("quote_manager:project_blacklist_list")
    
class ProjectBlacklistUpdateView(UpdateView):
    model = ProjectBlacklist
    template_name = "quote_manager/project_blacklist_update.html"
    fields = [
        "project",
        "reason",
    ]

class ProjectBlacklistDeleteView(DeleteView):
    model = ProjectBlacklist
    template_name = "quote_manager/project_blacklist_delete.html"
    success_url = reverse_lazy("quote_manager:project_blacklist_list")

##### COMPANY BLACKLIST #####
class CompanyBlacklistListView(ListView):
    model = CompanyBlacklist
    template_name = "quote_manager/company_blacklist_list.html"
    context_object_name = "blacklist_company_list"
    
class CompanyBlacklistDetailView(DetailView):
    model = CompanyBlacklist
    template_name = "quote_manager/company_blacklist_detail.html"
    context_object_name = "blacklist_company"

class CompanyBlacklistCreateView(CreateView):
    model = CompanyBlacklist
    template_name = "quote_manager/company_blacklist_create.html"
    fields = [
        "company",
        "reason",
    ]
    context_object_name = "blacklist_company"
    success_url = reverse_lazy("quote_manager:company_blacklist_detail")
    
class CompanyBlacklistUpdateView(UpdateView):
    model = CompanyBlacklist
    template_name = "quote_manager/company_blacklist_update.html"
    fields = [
        "company",
        "reason",
    ]
    context_object_name = "blacklist_company"
    success_url = reverse_lazy("quote_manager:company_blacklist_detail")

class CompanyBlacklistDeleteView(DeleteView):
    model = CompanyBlacklist
    template_name = "quote_manager/company_blacklist_delete.html"
    context_object_name = "blacklist_company"
    success_url = reverse_lazy("quote_manager:company_blacklist_list")
