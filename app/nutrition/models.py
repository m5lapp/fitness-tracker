from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

class TargetIntake(models.Model):
    """ A TargetIntake is is the daily amount of a number of key nutrients that
    the user is aiming for. The default values are based on the EU's Reference
    Intake recommendations for an average adult.
    """
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=4096, null=True, blank=True)
    energy = models.FloatField(
        default=2000.0,
        validators=[MinValueValidator(1000.0), MaxValueValidator(10000.0)],
        help_text=_('Daily target intake of energy in kcal'),
    )
    fat = models.FloatField(
        default=70.0,
        validators=[MinValueValidator(35.0), MaxValueValidator(350.0)],
        help_text=_('Daily target intake of fat in grams'),
    )
    saturates = models.FloatField(
        default=20.0,
        validators=[MinValueValidator(10.0), MaxValueValidator(100.0)],
        help_text=_('Daily target intake of saturated fat in grams'),
    )
    carbohydrates = models.FloatField(
        default=260.0,
        validators=[MinValueValidator(130.0), MaxValueValidator(1300.0)],
        help_text=_('Daily target intake of carbohydrates in grams'),
    )
    sugars = models.FloatField(
        default=90.0,
        validators=[MinValueValidator(45.0), MaxValueValidator(450.0)],
        help_text=_('Daily target intake of sugars in grams'),
    )
    protein = models.FloatField(
        default=50.0,
        validators=[MinValueValidator(25.0), MaxValueValidator(250.0)],
        help_text=_('Daily target intake of protein in grams'),
    )
    salt = models.FloatField(
        default=6.0,
        validators=[MinValueValidator(3.0), MaxValueValidator(30.0)],
        help_text=_('Daily maximum intake of salt in grams'),
    )

    class meta:
        ordering = ["name",]

    def __str__(self):
        return (f'{self.name[:50]}: {self.energy:.0f}kcal, '
                f'{self.fat:.0f}g fat, {self.protein:.0f}g protein')

class FoodCategory(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=256)

    class meta:
        ordering = ["name",]
        verbose_name_plural = 'Food categories'

    def __str__(self):
        return f'{self.name[:50]}'

class FoodItem(models.Model):
    """ TBD
    """
    UNITS = (
        ('g',     'grams'),
        ('units', 'items/pieces'),
        ('ml',    'millilitres'),
    )
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=256)
    category = models.ForeignKey(FoodCategory, on_delete=models.PROTECT)
    subcategory = models.CharField(max_length=256, null=True, blank=True)
    brand = models.CharField(max_length=256, null=True, blank=True)
    range = models.CharField(max_length=256, null=True, blank=True)
    notes = models.CharField(max_length=4096, null=True, blank=True)
    favourite = models.BooleanField(default=False)
    amount = models.FloatField(
        default=100.0,
        validators=[MinValueValidator(0.1), MaxValueValidator(10000.0)],
        help_text=_(''),
    )
    unit = models.CharField(max_length=10, choices=UNITS, default=UNITS[0][0])
    energy = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)],
        help_text=_('Calories (kcal) of energy per given amount'),
    )
    fat = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)],
        help_text=_('Grams of total fats per given amount'),
    )
    saturates = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)],
        help_text=_('Grams of saturated fat per given amount'),
    )
    carbohydrates = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)],
        help_text=_('Grams of carbohydrates per given amount'),
    )
    sugars = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)],
        help_text=_('Grams of carbohydrates of which sugars per given amount'),
    )
    protein = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)],
        help_text=_('Grams of protein per given amount'),
    )
    salt = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)],
        help_text=_('Grams of salt per given amount'),
    )

    class meta:
        ordering = [
            "-favourite", "category__name", "subcategory", "brand", "range",
            "name",
        ]

    def __str__(self):
        s = f'{self.category.name[:50]} | '

        if self.favourite:
            s = f'⭐ {s}'

        if self.subcategory:
            s += f'{self.subcategory[:50]} | '
        if self.brand:
            s += f'{self.brand[:50]} | '
        if self.range:
            s += f'{self.range[:50]} | '

        return f'{s}{self.name[:50]} ({self.unit})'

    def energy_kj(self):
        """ Convert the energy amount in kilocalories (kcal) to kilojoules (kJ).
        """
        return self.energy * 4.184

class Meal(models.Model):
    TYPES = (
        ('Breakfast',  '🥣 Breakfast'),
        ('Brunch',     '🍳 Brunch'),
        ('Desert',     '🍰 Desert'),
        ('Dinner',     '🍲 Dinner'),
        ('Drink',      '🥛 Drink'),
        ('Ingredient', '🥚 Ingredient'),
        ('Lunch',      '🥪 Lunch'),
        ('Snack',      '🥨 Snack'),
        ('Supplement', '🥫 Supplement'),
        ('Treat',      '🍪 Treat'),
    )
    date = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=10, choices=TYPES, default=TYPES[3][0])

    class meta:
        ordering = ["date",]

    def __str__(self):
        return f'{self.date.strftime("%Y-%m-%d %H:%M")} - {self.type}'

class MealItem(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    meal = models.ForeignKey(Meal, on_delete=models.PROTECT)
    food_item = models.ForeignKey(FoodItem, on_delete=models.PROTECT)
    amount = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)],
        help_text=_('Quantity of the item consumed'),
    )

    class meta:
        ordering = ["added",]

    def __str__(self):
        return f'{self.meal.__str__()[:50]}, {self.food_item.name[:50]}'
