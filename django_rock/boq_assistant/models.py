from django.db import models

class MCFModel(models.Model):
    mc_file = models.FileField("maxcut_file")
    datetime = models.DateTimeField("upload_datetime")
    msg = models.TextField("generator_message")
    gen_file = models.FileField("generated_file")
    
# class QuoteFileModel(models.Model):
#     quote_file = models.FileField("quote_file")
#     date = models.DateTimeField("upload_datetime")
#     gen_file = models.FileField("generated_file")
    
