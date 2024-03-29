from django import forms
from django_countries import countries
from .models import Review, Beer, Brewery, Address
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'step': '0.1', 
                'min': '0', 
                'max': '5', 
                'class': 'form-control',  # classe Bootstrap
            }),
            'comment': forms.Textarea(attrs={
                'rows': 4, 
                'cols': 40, 
                'class': 'form-control'  # classe Bootstrap
            }),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 0 or rating > 5:
            raise forms.ValidationError("Rating must be between 0 and 5.")
        return rating

class BeerForm(forms.ModelForm):
    class Meta:
        model = Beer
        fields = ['name', 'picture', 'brewery', 'style', 'abv', 'ibu', 'srm', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'style': forms.Select(attrs={'class': 'form-control'}),
            'abv': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1'
            }),
            'ibu': forms.NumberInput(attrs={'class': 'form-control'}),
            'srm': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control'
            }),
        }

    def clean_abv(self):
        abv = self.cleaned_data.get('abv')
        return abv

class BreweryForm(forms.ModelForm):
    line1 = forms.CharField(max_length=255, label="Address Line 1")
    line2 = forms.CharField(max_length=255, required=False, label="Address Line 2")
    city = forms.CharField(max_length=255)
    region = forms.CharField(max_length=255, required=False, label="State/Province/Region")
    postal_code = forms.CharField(max_length=12)
    country = forms.ChoiceField(choices=[(country.code, country.name) for country in countries])

    class Meta:
        model = Brewery
        fields = ['name', 'picture', 'line1', 'line2', 'city', 'region', 'postal_code', 'country']

    def save(self, commit=True):
        # Override o método save para poder criar e salvar o endereço
        brewery = super().save(commit=False)
        address = Address(
            line1=self.cleaned_data['line1'],
            line2=self.cleaned_data['line2'],
            city=self.cleaned_data['city'],
            region=self.cleaned_data['region'],
            postal_code=self.cleaned_data['postal_code'],
            country=self.cleaned_data['country']
        )
        if commit:
            address.save()
            brewery.address = address
            brewery.save()
        return brewery

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']