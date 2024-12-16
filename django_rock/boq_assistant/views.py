from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.http import HttpResponse, Http404
from django.conf import settings
from django.urls import reverse_lazy
import os
from .models import MCFModel, QFModel
from .forms import MCFForm, QFForm

def my_view(request):
    return HttpResponse("My view")

# --- MaxCutFile Views
class MCFListView(ListView):
    model = MCFModel
    template_name = "boq_assistant/mcf_list.html"
    context_object_name = "mcfs"
    
class MCFDetailView(DetailView):
    model = MCFModel
    template_name = "boq_assistant/mcf_detail.html"
    
class MCFCreateView(CreateView):
    model = MCFModel
    form_class = MCFForm
    template_name = "boq_assistant/mcf_create.html"
    success_url = reverse_lazy("mcf_list")
    
    ### TODO: implement file path validation to ensure existing files dont get deleted
    def form_valid(self, form):
        # if form.is_valid():
        obj = form.save(commit=False)
        path = settings.MEDIA_ROOT + "/test_file.txt"
        with open(path, "wt") as f:
            f.write("1234\n")
            
        # datetime set automatically
        obj.gen_file.name = path
        obj.warnings = "No warnings"
        print(obj.gen_file)
        obj.save()
        return super().form_valid(form)
    
class MCFDeleteView(DeleteView):
    model = MCFModel
    template_name = "boq_assistant/mcf_delete.html"
    success_url = reverse_lazy("mcf_list")
    
# --- QuoteFile Views
class QFListView(ListView):
    model = QFModel
    template_name = "boq_assistant/qf_list.html"
    context_object_name = "qfs"
    
class QFDetailView(DetailView):
    model = QFModel
    template_name = "boq_assistant/qf_detail.html"
    
class QFCreateView(CreateView):
    model = QFModel
    form_class = QFForm
    template_name = "boq_assistant/qf_create.html"
    success_url = reverse_lazy("qf_list")
    
    ### TODO: implement file path validation to ensure existing files dont get deleted
    def form_valid(self, form):
        # if form.is_valid():
        obj = form.save(commit=False)
        path = settings.MEDIA_ROOT + "/test_file.txt"
        with open(path, "wt") as f:
            f.write("1234\n")
            
        # datetime set automatically
        obj.gen_file.name = path
        obj.warnings = "No warnings"
        print(obj.gen_file)
        obj.save()
        return super().form_valid(form)
    
class QFDeleteView(DeleteView):
    model = QFModel
    template_name = "boq_assistant/qf_delete.html"
    success_url = reverse_lazy("qf_list")
    

