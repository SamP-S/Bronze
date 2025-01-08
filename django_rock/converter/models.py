from django.db import models
from django import forms

# TODO: validate uploaded file according to conversion selected
def validate_file_extension(value):
    valid_ext = ".csv"
    if not value.name.endswith(valid_ext):
        raise forms.ValidationError(f"File type not supported. Must be {valid_ext}")
# field = models.FileField("csv_file", validators=[validate_file_extension])


class FileConvertModel(models.Model):
    # user
    conversion = models.CharField(
        max_length=64,
        choices=[
            ('quote_xl_to_maxcut_zip', 'Quote.xlsx to MaxCut_CSVs.zip'),
            ('maxcut_csv_to_quote_xl', 'MaxCut.csv to Quote.xlsx')
            # add support for mc3 files
        ],
        default='quote_xl_to_maxcut_zip'
    )
    upload_file = models.FileField("upload_file")
    notes = models.TextField("notes", default="", blank=True, null=False)
    
    # meta data
    filename = models.CharField("filename", max_length=255, default="bad_name.txt")
    
    # generated
    gen_file = models.FileField("generated_file", blank=True, null=True)    # must support null files incase gen fails
    warnings = models.TextField("warnings", default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    # def __str__(self):
    #     return self.file.name