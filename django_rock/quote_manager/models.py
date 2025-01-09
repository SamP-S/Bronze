from django.db import models

class ProjectModel(models.Model):
    address = models.CharField(max_length=255)
    # TODO: add auto address from postcode
    postcode = models.CharField(max_length=16, default="", blank=True)
    
    WORK_TYPE_CHOICES = [
        ("unknown", "Unknown"),
        ("tiling", "Tiling"),
        ("stone", "Stone"),
        ("joinery", "Joinery"),
        ("mixed", "Mixed"),
    ]
    work_type = models.CharField(
        max_length=255,
        choices=WORK_TYPE_CHOICES,
        default="unknown"
    )
    value = models.FloatField(default=0.0, blank=True)
    
    CONTRACT_TYPE_CHOICES = [
        ("unknown", "Unknown"),
        ("tender", "Tender"),
        ("contract", "Contract"),
    ]
    contract_type = models.CharField(
        max_length=255,
        choices=CONTRACT_TYPE_CHOICES,
        default="unknown",
    )
    
    # optional
    # TODO: consider replacing with custom user model
    estimater = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="project_estimater")
    manager = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="project_manager")
    
    # generated
    # TODO: add a created by to track who filled in the new quote
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attractiveness = models.IntegerField(blank=True, null=True)
    multiplier = models.IntegerField(blank=True, null=True)
    chasability = models.IntegerField(blank=True, null=True)
    last_reminder_at = models.DateTimeField(blank=True, null=True)

### NOTE:
# currently company is dumped in the quote request as the only unique company info is the name
# not ideal but otherwise you have a dumb model
    
class QuoteModel(models.Model):
    # blank allows for empty strings or default values to be used
    # null allows for not setting a value
    
    # TODO: consider safety of using this?
    # on_delete=models.CASCADE means that if the project is deleted, the quote request is also deleted
    
    # required
    # TODO: add a created by to track who filled in the quote
    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE)
    company = models.CharField(max_length=255, blank=False, null=False)
    contact_name = models.CharField(max_length=255, blank=False, null=False)
    contact_email = models.EmailField(blank=False, null=False)
    date_in = models.DateField(blank=False, null=False)
    QUOTE_STATE_CHOICES = [
        ("unknown", "Unknown"),
        ("incomplete", "Incomplete"),
        ("unclaimed", "Unclaimed"),
        ("in_progress", "In progress"),
        ("waiting_for_supplier", "Waiting for supplier"),
        ("waiting_for_client", "Waiting for client"),
        ("sent", "Sent"),
        ("to_chase", "To Chase"),
    ]
    state = models.CharField(max_length=255, choices=QUOTE_STATE_CHOICES, default="unknown", blank=False, null=False)
    state_updated_at = models.DateTimeField(blank=True, null=True)
    
    # optional
    contact_phone = models.CharField(max_length=16, blank=True, null=True)
    date_close = models.DateField(blank=True, null=True)
    date_sent = models.DateField(blank=True, null=True)
    BUISNESS_BY_CHOICES = [
        ("karl", "Karl"),
        ("scs", "SCS"),
    ]
    buisness_by = models.CharField(max_length=255, choices=BUISNESS_BY_CHOICES, blank=True, null=True)
    
    # generated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    

class ProjectBlacklist(models.Model):
    # required
    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255, blank=False, null=False)
    
    # generated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Project Blacklist ({self.id}) - {self.project.address} ({self.project.id})"
    
    

class CompanyBlacklist(models.Model):
    # required
    company = models.CharField(max_length=255, blank=False, null=False)
    reason = models.CharField(max_length=255, blank=False, null=False)
    
    # generated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Company Blacklist ({self.id}) - {self.company}"
    