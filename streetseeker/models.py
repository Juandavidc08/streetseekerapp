from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Place(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    date_reserved = models.DateTimeField(auto_now_add=True)
    date_of_visit = models.DateField()
    time_of_visit = models.TimeField()

    def __str__(self):
        return f"{self.user.username} - {self.place.title} on {self.date_of_visit}"

class Comment(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.reservation.place.title}"