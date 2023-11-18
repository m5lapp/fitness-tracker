from django.core.exceptions import ValidationError
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
    active = models.BooleanField(default=False)
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

    class Meta:
        ordering = ["name",]

    def __str__(self):
        return (f'{self.name[:50]}: {self.energy:.0f}kcal, '
                f'{self.fat:.0f}g fat, {self.protein:.0f}g protein')

    @classmethod
    def current(cls):
        try:
            return cls.objects.filter(active=True).latest("updated")
        except TargetIntake.DoesNotExist:
            return None

class FoodCategory(models.Model):
    """ FoodCategory simply represents a high-level categorization of foods and
    beverages.
    """
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=256)

    class Meta:
        ordering = ["name",]
        verbose_name_plural = 'Food categories'

    def __str__(self):
        return f'{self.name[:50]}'

class FoodItem(models.Model):
    """ FoodItem represents an item of food or drink from a single ingredient
    up to a full meal. The nutritional information is stored for a given
    reference unit quantity, such as 100g, 100ml, 1 item, 1 biscuit etc.
    """
    UNITS = (
        ('g',        'grams'),
        ('units',    'items/pieces'),
        ('ml',       'millilitres'),
        ('servings', 'servings/portions'),
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
    unit_quantity = models.FloatField(
        default=100.0,
        validators=[MinValueValidator(0.1), MaxValueValidator(10000.0)],
        help_text=_('The unit quantity for which the nutritional values apply'),
    )
    unit_units = models.CharField(
        max_length=10, choices=UNITS, default=UNITS[0][0],
        help_text=_('The units used to measure the unit quantity'),
    )
    energy = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)],
        help_text=_('Calories (kcal) of energy per unit quantity'),
    )
    fat = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)],
        help_text=_('Grams of total fats per unit quantity'),
    )
    saturates = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)],
        help_text=_('Grams of saturated fat per unit quantity'),
    )
    carbohydrates = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)],
        help_text=_('Grams of carbohydrates per unit quantity'),
    )
    sugars = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)],
        help_text=_('Grams of carbohydrates of which sugars per unit quantity'),
    )
    protein = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)],
        help_text=_('Grams of protein per unit quantity'),
    )
    salt = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)],
        help_text=_('Grams of salt per unit quantity'),
    )

    class Meta:
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

        return f'{s}{self.name[:50]} ({self.unit_units})'

    def clean(self):
        errors = {}
        msg = 'The amount of {0} cannot be greater than the amount of {1}'

        if self.saturates and self.fat:
            if self.saturates > self.fat:
                errors['saturates'] = msg.format('saturated fat', 'fat')
        if self.sugars and self.carbohydrates:
            if self.sugars > self.carbohydrates:
                errors['sugars'] = msg.format('sugars', 'carbohydrates')

        if errors:
            raise ValidationError(errors)

    def energy_kj(self):
        """ Convert the energy amount in kilocalories (kcal) to kilojoules (kJ).
        """
        return self.energy * 4.184

class Journal(models.Model):
    """ Journal represents a collection of one or more JournalItems of food or
    drink consumed over a single day.
    """
    date = models.DateField(default=timezone.now, unique=True)
    notes = models.TextField(max_length=4096, null=True, blank=True)
    items = models.ManyToManyField(FoodItem, through="JournalItem")

    class Meta:
        ordering = ["date",]

    def __str__(self):
        n = self.nutrition()
        target = TargetIntake.current()
        target_met_emoji = ''

        if target:
            if self.target_intake_met(target):
                target_met_emoji = '🟢 '
            else:
                target_met_emoji = '🔴 '

        return (
            f'{self.date} | {target_met_emoji}'
            f'{n["energy"]:.0f}kcal, '
            f'{n["fat"]:.1f}/{n["saturates"]:.1f}g fat/sats., '
            f'{n["carbohydrates"]:.1f}/{n["sugars"]:.1f}g carbs/sugars, '
            f'{n["protein"]:.1f}g protein, {n["salt"]:.2f}g salt'
        )
    
    def nutrition(self):
        energy = fat = sat = carbs = sugars = protein = salt = 0
        for item in JournalItem.objects.filter(journal=self):
            energy += (item.energy() or 0)
            fat += (item.fat() or 0)
            sat += (item.saturates() or 0)
            carbs += (item.carbohydrates() or 0)
            sugars += (item.sugars() or 0)
            protein += (item.protein() or 0)
            salt += (item.salt() or 0)
        return {
            'energy': None or energy,
            'fat': None or fat,
            'saturates': None or sat,
            'carbohydrates': None or carbs,
            'sugars': None or sugars,
            'protein': None or protein,
            'salt': None or salt,
        }

    def target_intake_met(self, target: TargetIntake, deviation: float=0.05) -> bool:
        def within_deviation(value, target) -> bool:
            """ Check a given value is with a given deviation percentage of a
            target value (plus or minus).
            """
            return abs(target - value) <= target * deviation

        n = self.nutrition()
        print(self.date,    within_deviation(n['energy'], target.energy))
        print(self.date,    within_deviation(n['fat'], target.fat))
        print(self.date,    within_deviation(n['saturates'], target.saturates))
        print(self.date,    within_deviation(n['carbohydrates'], target.carbohydrates))
        print(self.date,    within_deviation(n['sugars'], target.sugars))
        print(self.date,    within_deviation(n['protein'], target.protein))
        print(self.date,    n['salt'] <= target.salt)
        return (
            within_deviation(n['energy'], target.energy) and
            within_deviation(n['fat'], target.fat) and
            within_deviation(n['saturates'], target.saturates) and
            within_deviation(n['carbohydrates'], target.carbohydrates) and
            within_deviation(n['sugars'], target.sugars) and
            within_deviation(n['protein'], target.protein) and
            n['salt'] <= target.salt
        )

    
class JournalItem(models.Model):
    """ JournalItem is an instance of a FoodItem consumed on a particular
    Journal day. The quantity consumed is recorded and used to calculate the
    total nutritional value based on the unit quantity value in the FoodItem.
    """
    TYPES = {
        'Breakfast':  '🥣 Breakfast',
        'Brunch':     '🍳 Brunch',
        'Desert':     '🍰 Desert',
        'Dinner':     '🍲 Dinner',
        'Drink':      '🥛 Drink',
        'Ingredient': '🥚 Ingredient',
        'Lunch':      '🥪 Lunch',
        'Snack':      '🥨 Snack',
        'Supplement': '🥫 Supplement',
        'Treat':      '🍪 Treat',
    }
    TYPE_CHOICES = tuple((k, v,) for k, v in TYPES.items())
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    journal = models.ForeignKey(Journal, on_delete=models.PROTECT)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='Dinner')
    quantity = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)],
        help_text=_('Quantity of the food item that was consumed'),
    )
    food_item = models.ForeignKey(FoodItem, on_delete=models.PROTECT)

    class Meta:
        ordering = ["added",]

    def __str__(self):
        return (
            f'{self.journal.date} | {self.TYPES[self.type]} | '
            f'{self.food_item.name[:50]} ({self.energy()}kcal '
            f'{self.fat():.1f}/{self.saturates():.1f}g fat/sats., '
            f'{self.carbohydrates():.1f}/{self.sugars():.1f}g carbs/sugars, '
            f'{self.protein():.1f}g protein, {self.salt():.2f}g salt)'
        )

    def get_nutrition_amount(self, unit_nutrient_quantity):
        if unit_nutrient_quantity == None:
            return 0
        return self.quantity / self.food_item.unit_quantity * unit_nutrient_quantity 

    def energy(self):
        return self.get_nutrition_amount(self.food_item.energy)

    def fat(self):
        return self.get_nutrition_amount(self.food_item.fat)

    def saturates(self):
        return self.get_nutrition_amount(self.food_item.saturates)

    def carbohydrates(self):
        return self.get_nutrition_amount(self.food_item.carbohydrates)

    def sugars(self):
        return self.get_nutrition_amount(self.food_item.sugars)

    def protein(self):
        return self.get_nutrition_amount(self.food_item.protein)

    def salt(self):
        return self.get_nutrition_amount(self.food_item.salt)
