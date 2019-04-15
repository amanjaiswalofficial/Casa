import re

from django import forms
from django.forms import ModelForm
from django.forms import ModelForm
from .models import PropertyImages,Property
invalid_entries = ['', ' ', '-', '%', '&', '*', '^', '~', '!', '@', '$']
ERROR_MESSAGE = 'Invalid entry, please try again with a valid input'
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
        price = re.compile("^[\d]{4,}$")

        if not re.match(patter_number, str(cd.get("property_pin"))):
            self.add_error('property_pin', "The pin code must be a 6 digit number")

        if not re.match(price, str(cd.get("property_price"))):
            self.add_error('property_price', "The price must be at least above 1000")

        for field in self.fields:
            if str(cd.get(field)) in invalid_entries:
                self.add_error(field, ERROR_MESSAGE)

