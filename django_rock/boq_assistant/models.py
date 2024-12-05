from django.db import models

class MaxCutFileModel(models.Model):
    mc_file = models.FileField("maxcut_file")
    date = models.DateTimeField("upload_datetime")
    gen_file = models.FileField("generated_file")
    
class QuoteFileModel(models.Model):
    quote_file = models.FileField("quote_file")
    date = models.DateTimeField("upload_datetime")
    gen_file = models.FileField("generated_file")
    
