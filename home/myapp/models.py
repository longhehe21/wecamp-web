from django.db import models

class Tour(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    destination = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Booking(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    checkin = models.DateField()
    checkout = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.tour.name}"

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email