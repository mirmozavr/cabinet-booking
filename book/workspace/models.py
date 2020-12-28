from django.contrib.auth.models import User
from django.db import models


class Cabinet(models.Model):
    room_number = models.IntegerField()

    def __str__(self):
        return f"Cab.№ {self.room_number}"


class Booking(models.Model):
    booking_start = models.DateField()
    booking_end = models.DateField()
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.booking_start} - {self.booking_end} by {self.customer}"

    def intersect(self, other_booking):
        if self.booking_start > other_booking.booking_end or self.booking_end < other_booking.booking_start:
            return False
        return True
