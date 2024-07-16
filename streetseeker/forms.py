from django import forms
from .models import Reservation, Comment

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['place', 'date_of_visit']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
