from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

class MeasurementType(models.Model):
    """ MeasurementType represents anything that can be measured such as weight,
    blood pressure, heart rate or waist.
    """
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=256, unique=True)
    unit = models.CharField(
        max_length=32,
        help_text=_('The full name of the unit of measurement'),
    )
    symbol = models.CharField(
        max_length=16,
        help_text=_('The symbol for the unit of measurement'),
    )
    description = models.CharField(max_length=4096, null=True, blank=True)

    def __str__(self):
        return f'{self.name[:50]} ({self.unit})'

class Measurement(models.Model):
    """ Measurement represents a recording of a particular measurement type at a
    given point in time.
    """
    date = models.DateTimeField(default=timezone.now)
    type = models.ForeignKey(MeasurementType, on_delete=models.PROTECT)
    measurement = models.FloatField(
        validators=[MinValueValidator(0.0)],
        help_text=_('The value of the measurement taken'),
    )
    notes = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return f'{self.type.name[:50]} - {self.measurement}{self.type.symbol}'
