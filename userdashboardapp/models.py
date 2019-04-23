from django.db import models
from propertyapp.models import Enquiry


class QueryResponses(models.Model):
    enquiry_made = models.ForeignKey(Enquiry, on_delete=models.CASCADE)
    response = models.CharField(max_length=200)