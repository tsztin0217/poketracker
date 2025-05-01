from django import forms
from .models import UserCardInfo

class UserCardInfoForm(forms.ModelForm):
    class Meta:
        model = UserCardInfo
        fields = [
            'date_obtained', 
            'method_obtained', 
            'price_paid',
            'graded',
            'grade', 
            'comments'
            ]
        widgets = {
            'date_obtained': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'placeholder': 'Select a date',
                    'type': 'date'
                }
            ),
        }