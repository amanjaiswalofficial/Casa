import re

from django import forms
from django.forms import ModelForm
from django.forms import ModelForm
from .models import PropertyImages,Property

class PropertyImagesForm(ModelForm):


    Property_Images=forms.ImageField()

    class Meta:
        model = PropertyImages
        fields = []

class NewPropertyForm(ModelForm):


    class Meta:
        model = Property
        fields = [
            'property_title',
            'property_address',
            'property_pin',
            'property_price',
            'property_bedroom',
            'property_bathroom',
            'property_sq_feet',
            'property_lot_size',
            'property_garage',
            'property_description',
        ]

    def clean(self):
        cd = self.cleaned_data

        patter_number = re.compile("^[\d]{6}$")

        if not re.match(patter_number, str(cd.get("property_pin"))):
            self.add_error('property_pin', "The pin code must be a 6 digit number")

