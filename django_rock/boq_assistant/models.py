from django.db import models
from django import forms
from django.utils import timezone

def validate_file_is_csv(value):
    if not value.name.endswith(".csv"):
        raise forms.ValidationError("File type not supported")
    
def validate_file_is_excel(value):
    if not value.name.endswith(".xlsx"):
        raise forms.ValidationError("File type not supported")

class MCFModel(models.Model):
    # user upload
    name = models.CharField("name", max_length=255, default="Unnamed")
    notes = models.TextField("notes", default="")
    mc_file = models.FileField("maxcut_file", validators=[validate_file_is_csv])
    
    # auto generated
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    warnings = models.TextField("warnings", default="")
    gen_file = models.FileField("generated_file")
    
    class Meta:
        ordering = ["-created_at"]

class QFModel(models.Model):
    # user upload
    name = models.CharField("name", max_length=255, default="Unnamed")
    notes = models.TextField("notes", default="")
    q_file = models.FileField("quote_file", validators=[validate_file_is_excel])
    
    # auto generated
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    warnings = models.TextField("warnings", default="")
    gen_file = models.FileField("generated_file")
    
    class Meta:
        ordering = ["-created_at"]