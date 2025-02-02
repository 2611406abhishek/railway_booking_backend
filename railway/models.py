from django.db import models
from django.contrib.auth.models import User

class Train(models.Model):
    train_number = models.CharField(max_length=50, unique=True)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.train_number}: {self.source} to {self.destination}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} by {self.user.username} on train {self.train.train_number}"
