from django import forms
from .models import MCFModel

class MCFForm(forms.ModelForm):
    class Meta:
        model = MCFModel
        
        # reference python variable names
        fields = [
            "name",
            "notes",
            "mc_file",
        ]
        
        # widgets = {
        #     "mc_file": forms.FileField(attrs={'class' : 'form-upload-file'}),
        #     "upload_datetime" : forms.DateTimeInput(attrs={"class" : "form-upload-datetime"})
        # }
        
