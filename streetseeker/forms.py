from django import forms
from .models import Reservation, Comment

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['place', 'date_of_visit', 'time_of_visit']
        widgets = {
            'date_of_visit': forms.DateInput(attrs={'type': 'date'}),
            'time_of_visit': forms.TimeInput(attrs={'type': 'time'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(label='Your Message', widget=forms.Textarea)
