from django import forms
from .models import MaxCutFileModel

class MaxCutForm(forms.ModelForm):
    class Meta:
        model = MaxCutFileModel
        
        fields = [
            "maxcut_file"
        ]
        
