from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

class Location(models.Model):
    """ Location represents a geographical place where an exercise session takes
    place, for example a gym or a park.
    """
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        ordering = ["name",]

    def __str__(self):
        return self.name[:50]

class SessionType(models.Model):
    """ SessionType describes a particular type of exercise session for example
    "lower body", "arms and chest" or "Parkrun".
    """
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(max_length=4096, null=True, blank=True)

    class Meta:
        ordering = ["name",]

    def __str__(self):
        return self.name[:50]

class Session(models.Model):
    """ Session represents a particular instance of an exercise session. """
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(default=timezone.now)
    session_type = models.ForeignKey(SessionType, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    notes = models.TextField(max_length=65536, null=True, blank=True)

    class Meta:
        ordering = ["-date", "session_type",]

    def __str__(self):
        return f'{self.date.strftime("%Y-%m-%d")}: {self.session_type}'

class Exercise(models.Model):
    """ Exercise represents a single type of exercise activity such as running,
    leg curls, sit ups or yoga.
    """
    TYPES = (
        ('Aerobic', 'Aerobic (cardiovascular)'),
        ('Anaerobic', 'Anaerobic (strengthening)'),
        ('Flexibility', 'Flexibility'),
    )
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=256, unique=True)
    type = models.CharField(max_length=11, choices=TYPES, default=TYPES[1][0])
    description = models.TextField(max_length=4096, null=True, blank=True)

    class Meta:
        ordering = ["name",]

    def __str__(self):
        return self.name

class SessionExercise(models.Model):
    """ SessionExercise represents an instance of a single type of exercise
    performed within an exercise session.
    """
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    session = models.ForeignKey(Session, on_delete=models.PROTECT)
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    duration = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(60 * 60 * 24 * 7)],
        help_text=_('Time taken in seconds'),
    )
    distance = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(1_000_000)],
        help_text=_('Distance covered in metres'),
    )
    calories = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10_000)],
        help_text=_('Calories (kcal) burned'),
    )
    weight = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(-1000.0), MaxValueValidator(1000.0)],
        help_text=_('Weight used in kg, negative implies weighted assistance'),
    )
    sets = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text=_('Number of sets completed'),
    )
    reps = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(1_000_000)],
        help_text=_('Number of repetitions per set'),
    )
    notes = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        ordering = ["session", "added",]

    def __str__(self):
        duration = distance = calories = weight = sets = reps = ''

        if self.duration:
            duration = f'{self.duration}s, '
        if self.distance:
            distance = f'{self.distance}m, '
        if self.calories:
            calories = f'{self.calories}kcal, '
        if self.weight:
            weight = f'{self.weight}kg '
        if self.sets:
            sets = f'× {self.sets} sets '
        if self.reps:
            reps = f'× {self.reps} reps'

        s = (
            f'{self.exercise.name[:20]}: '
            f'{duration}{distance}{calories}{weight}{sets}{reps}'
        )
        return s.rstrip(', ')
