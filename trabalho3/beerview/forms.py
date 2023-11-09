from django import forms
from .models import Review, Beer

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'step': '0.1', 'min': '0', 'max': '5'}),
            'comment': forms.Textarea(attrs={'rows': 4, 'cols': 40})
        }

class BeerForm(forms.ModelForm):
    class Meta:
        model = Beer
        fields = ['name', 'brewery', 'style', 'abv', 'ibu', 'srm', 'description']