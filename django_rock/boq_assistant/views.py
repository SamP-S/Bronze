from django.shortcuts import render
from django.views import View, generic
from django.http import HttpResponse, Http404
from django.conf import settings
import os

def DownloadFile(request, path):
    print(request)
    full_path = os.path.join(settings.MEDIA_ROOT, path)
    if (not os.path.exists(full_path)):
        return Http404()
    with open(full_path, "rb") as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")  
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(full_path)
        return response


class MyView(View):
    def get(self, request):
        return HttpResponse("My view")

