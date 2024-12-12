from django.db import models

class ProjectModel(models.Model):
    address = models.CharField(max_length=255, blank=False, null=False)
    # TODO: add auto address from postcode
    postcode = models.CharField(max_length=16, blank=True, null=False)
    in_london = models.BooleanField(default=False, blank=False, null=False)
    
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
        default="unknown",
        blank=False,
        null=False
    )
    value = models.IntegerField()
    
    CONTRACT_TYPE_CHOICES = [
        ("unknown", "Unknown"),
        ("tender", "Tender"),
        ("contract", "Contract"),
    ]
    contract_type = models.CharField(
        max_length=255,
        choices=CONTRACT_TYPE_CHOICES,
        default="unknown",
        blank=False,
        null=False
    )
    
    # generated
    created_at = models.DateTimeField(auto_now_add=True)
    attractiveness = models.IntegerField()
    multiplier = models.IntegerField()
    chasability = models.IntegerField()
    
    
class QuoteRequestModel(models.Model):
    # blank allows for empty strings or default values to be used
    # null allows for not setting a value
    
    # TODO: consider safety of using this?
    # on_delete=models.CASCADE means that if the project is deleted, the quote request is also deleted
    
    # required
    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE)
    company = models.CharField(max_length=255, blank=False, null=False)
    contact_name = models.CharField(max_length=255, blank=False, null=False)
    contact_email = models.EmailField(blank=False, null=False)
    date_in = models.DateField(blank=False, null=False)
    
    # optional
    contact_phone = models.CharField(max_length=16, blank=True, null=True)
    date_close = models.DateField(blank=False, null=False)
    date_sent = models.DateField(blank=True, null=True)
    
    # generated
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    