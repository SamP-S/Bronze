from django import forms

from .models import FileConvertModel

# replace Model form with custom form for much nicer looking and more intuitive
class FileConvertForm(forms.ModelForm):
    class Meta:
        model = FileConvertModel
        fields = ['conversion', 'upload_file', 'notes']
        
        # TODO: figure out what widgets are
        # widgets = {"upload_file": forms.FileField(attrs={'class' : 'form-upload-file'})}
