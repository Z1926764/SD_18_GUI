from django.db import models

class PressurePoint(models.Model):
    time = models.CharField(max_length=255)
    Spressure = models.CharField(max_length=255, null=True)
    Cpressure = models.CharField(max_length=255, null=True)
    switchState = models.CharField(max_length=255, null=True)

class GlobalValues(models.Model):
    pMesDelta = models.DecimalField(decimal_places=6, max_digits=10, default=1.00)
    setPoint = models.DecimalField(decimal_places=2, max_digits=6, default=1.00)
    currentSPressure = models.DecimalField(decimal_places=2, max_digits=6, default=1.00)
    currentCPressure = models.DecimalField(decimal_places=2, max_digits=6, default=1.00)
    dutyCycle = models.DecimalField(decimal_places=2, max_digits=6, default=1.00)