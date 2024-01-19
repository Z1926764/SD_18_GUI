from django.db import models

class PressurePoint(models.Model):
    time = models.CharField(max_length=255)
    pressure = models.CharField(max_length=255)

class GlobalValues(models.Model):
    pMesDelta = models.DecimalField(decimal_places=6, max_digits=10, default=1.00)
    setPoint = models.DecimalField(decimal_places=2, max_digits=6, default=1.00)
    currentPressure = models.DecimalField(decimal_places=2, max_digits=6, default=1.00)