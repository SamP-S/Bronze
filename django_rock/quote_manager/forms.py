from django import forms
from .models import ProjectModel, QuoteRequestModel

class ProjectForm(forms.ModelForm):

    class Meta:
        model = ProjectModel
        fields = ['address', 'postcode', 'work_type', 'value', 'contract_type']

class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequestModel
        fields = ['company', 'date_in', 'date_close', 'date_sent', 'contact_name', 'contact_email', 'contact_phone', 'state', 'state_updated_at',]
