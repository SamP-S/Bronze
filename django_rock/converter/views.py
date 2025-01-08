from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.http import HttpResponse, Http404
from django.conf import settings
from django.urls import reverse_lazy
import os
from .models import FileConvertModel
from .forms import FileConvertForm
import scs

def my_view(request):
    return HttpResponse("My view")

# NOTE: file urls are all relative to MEDIA_ROOT
# i.e. <MEDIA_ROOT>"/dir/my_file.txt"
# returns valid_path, original filename
# TODO: move this to SCS util pkg under file
def get_valid_upload_path(path):
    # match django's filename auto formatting
    filename = os.path.basename(path).replace(" ", "_")
    parent_dir = os.path.dirname(path)
    format_path = os.path.join(parent_dir, filename)
    
    # ensure necessary subdir exists
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, parent_dir)):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, parent_dir), exist_ok=True)
    
    # catch guard for existing path
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, format_path)):
        return format_path, filename
    
    # file exists, generate new path sequentially
    # TODO: use random str generation for better performance
    base, extension = os.path.splitext(filename)
    count = 1
    new_filename = f"{base}_{count}{extension}"
    new_path = os.path.join(parent_dir, new_filename)
    while os.path.exists(os.path.join(settings.MEDIA_ROOT, new_path)):
        count += 1
        new_filename = f"{base}_{count}{extension}"
        new_path = os.path.join(parent_dir, new_filename)
    return new_path, filename
       

# --- QuoteFile Views
class FCListView(ListView):
    model = FileConvertModel
    template_name = "converter/fc_list.html"
    context_object_name = "fcs"
    
class FCDetailView(DetailView):
    model = FileConvertModel
    template_name = "converter/fc_detail.html"
    
class FCCreateView(CreateView):
    model = FileConvertModel
    form_class = FileConvertForm
    template_name = "converter/fc_create.html"
    success_url = reverse_lazy("fc_list")
    
    ### TODO: implement file path validation to ensure existing files dont get deleted
    # TODO: test what must be relative to root and what must be relative to MEDIA_ROOT
    # TODO: consider organising uploaded files by type->user->year->month
    def form_valid(self, form):
        obj = form.save(commit=False)
        
        ori_path = os.path.join("fc", obj.upload_file.name)
        print(f"original path = {ori_path}")
        obj.filename = os.path.basename(ori_path).replace(".xlsx", ".zip")
        
        new_path, ori_filename = get_valid_upload_path(ori_path)
        obj.upload_file.name = new_path
        
        # must save first to force uploaded file to download
        obj.save()
        
        # generate converted file
        rel_root_path = os.path.join(settings.MEDIA_ROOT, new_path)
        print(f"rel_root_path: {rel_root_path}")
        print(f"list dirs:\n {os.listdir(os.path.dirname(rel_root_path))}")
        
        print(f"path: {rel_root_path}")
        # TODO: apply conversion here according to selected
        # TODO: replace if-switch with dictionary look up
        gen_path = None
        if obj.conversion == "quote_xl_to_maxcut_zip":
            gen_path = scs.converters.quote_to_maxcut(rel_root_path)
        else:
            gen_path = scs.converters.maxcut_to_quote(rel_root_path)
        print(f"gen_path: {gen_path}")
        print(f"gen_path type: {type(gen_path)}")
        
        # Save the new file path to gen_file
        print(f"media_root: {settings.MEDIA_ROOT}")
        print(f"cwd: {os.getcwd()}")
        print(f"cwd type: {type(os.getcwd())}")
        gen_path = gen_path.replace(os.getcwd(), "")
        print(f"gen_path: {gen_path}")
        obj.gen_file.name = gen_path
        obj.warnings = "No warnings"
        print(f"generated file: {obj.gen_file}")
        
        return super().form_valid(form)
    
class FCDeleteView(DeleteView):
    model = FileConvertModel
    template_name = "converter/fc_delete.html"
    success_url = reverse_lazy("fc_list")
    

