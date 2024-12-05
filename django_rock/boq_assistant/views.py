from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, Http404
from django.conf import settings
from django.urls import reverse_lazy
import os
from .models import MCFModel
from .forms import MCFForm

# # absolutely no security validation taking place lol
# def DownloadFile(request, path):
#     print(request)
#     full_path = os.path.join(settings.MEDIA_ROOT, path)
#     if (not os.path.exists(full_path)):
#         return Http404()
#     with open(full_path, "rb") as fh:
#         response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")  
#         response['Content-Disposition'] = 'inline; filename=' + os.path.basename(full_path)
#         return response

class MCFListView(ListView):
    model = MCFModel
    template_name = "boq_assistant/mcf_list.html"
    context_object_name = "mcf"
    
class MCFDetailView(DeleteView):
    model = MCFModel
    template_name = "boq_assistant/mcf_detail.html"
    
class MCFCreateView(CreateView):
    model = MCFModel
    form_class = MCFForm
    template_name = "boq_assistant/mcf_create.html"
    success_url = reverse_lazy("mcf_list")
    
class MCFUpdateView(UpdateView):
    model = MCFModel
    form_class = MCFForm
    template_name = "boq_assistant/mcf_update.html"
    success_url = reverse_lazy("mcf_detail")
    
class MCFDeleteView(DeleteView):
    model = MCFModel
    template_name = "boq_assistant/mcf_delete.html"
    success_url = reverse_lazy("mcf_list")
    

class MyView(View):
    def get(self, request):
        return HttpResponse("My view")

