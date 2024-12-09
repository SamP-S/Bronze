from django.db import models
from django import forms

def validate_file_is_csv(value):
    if not value.name.endswith(".csv"):
        raise forms.ValidationError("File type not supported")

class MCFModel(models.Model):
    # user upload
    name = models.CharField("name", max_length=255, default="Unnamed")
    notes = models.TextField("notes", default="")
    mc_file = models.FileField("maxcut_file", validators=[validate_file_is_csv])
    
    # auto generated
    datetime = models.DateTimeField("upload_datetime", auto_now=True)
    warnings = models.TextField("generator_message", default="")
    gen_file = models.FileField("generated_file")
    
    class Meta:
        ordering = ["-datetime"]
    