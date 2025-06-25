from django.db import models

class MaintenanceLog(models.Model):
    date = models.DateField()
    vehicle = models.CharField(max_length=100)
    mileage = models.IntegerField()
    service = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.vehicle} - {self.service} on {self.date}"
