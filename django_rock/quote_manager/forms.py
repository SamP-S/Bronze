from django import forms
from .models import ProjectModel, QuoteModel

class ProjectForm(forms.ModelForm):
    
    class Meta:
        model = ProjectModel
        fields = ['address', 'postcode', 'work_type', 'contract_type', 'value', 'estimater', 'manager']



class QuoteForm(forms.ModelForm):
    
    class Meta:
        model = QuoteModel
        fields = ['company', 'date_in', 'date_close', 'date_sent', 'buisness_by', 'contact_name', 'contact_email', 'contact_phone', 'state', 'state_updated_at',]
