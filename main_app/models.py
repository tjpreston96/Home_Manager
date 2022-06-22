from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.forms import Textarea
from django.urls import reverse
from django.utils import timezone

# import pandas as pd

# Enables Translation
# from django.utils.translation import gettext_lazy as _


# ======== Field.choices ========
FREQUENCY = (
    (1, "Daily"),
    (3, "Biweekly"),
    (7, "Weekly"),
    (14, "Two Weeks"),
    (21, "Three Weeks"),
    (30, "Monthly"),
)

# ======== Validators ========
# Needs gettext_lazy formatting for translation
def validate_date(date):
    if date > timezone.now().date():
        raise ValidationError("Future scheduling is not currently available.")


# ======== Plant Model ========
class Plant(models.Model):
    class LightLevel(models.TextChoices):
        SHADE = "Shade"
        LOW = "Low"
        MODERATE = "Moderate"
        HIGH = "High"
        FULL_SUN = "Full Sun"

    class Environment(models.TextChoices):
        INDOOR = "Indoor"
        OUTDOOR = "Outdoor"

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    light = models.CharField(
        max_length=10, choices=LightLevel.choices, default=LightLevel.LOW
    )
    toxicity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    environment = models.CharField(
        max_length=7, choices=Environment.choices, default=Environment.INDOOR
    )
    watering_frequency = models.IntegerField(
        default=FREQUENCY[2][0],
        choices=FREQUENCY,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plants_detail", kwargs={"plant_id": self.id})

    def days_till(self):
        freq = self.watering_frequency
        last_maintenance = self.maintenance_set.first().date
        next_due_date = last_maintenance + timedelta(days=freq)
        return (next_due_date - date.today()).days

    class Meta:
        ordering = ["id"]


# ======== Photo Model (Plants) ========
class Photo(models.Model):
    url = models.CharField(max_length=200)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for plant_id: {self.plant_id} @{self.url}"


# ======== Maintenance Model (Plants) ========
class Maintenance(models.Model):
    class Nutrients(models.TextChoices):
        WATER = "W"
        NUTRIENT_FOAM = "F"

    date = models.DateField(validators=[validate_date])
    nutrients = models.CharField(
        max_length=20,
        choices=Nutrients.choices,
    )
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_nutrients_display()} on {self.date}"

    class Meta:
        ordering = ["-date"]


# ======== Tasks Model ========
class Task(models.Model):
    # category = models.CharField(max_length=100) <-- maybe?
    task = models.CharField(max_length=100)
    details = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.task} last updated on {self.updated}"

    def get_absolute_url(self):
        return reverse("tasks_detail", kwargs={"task_id": self.id})

    class Meta:
        ordering = ["-updated"]


# ======== Notes Model ========
class Note(models.Model):
    title = models.CharField(max_length=100)
    note = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} last updated on {self.updated}"

    def get_absolute_url(self):
        return reverse("notes_detail", kwargs={"note_id": self.id})

    class Meta:
        ordering = ["-updated"]


# ======== Shopping Model ========
class Shopping(models.Model):
    item = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item} added to list on {self.created}"

    class Meta:
        ordering = ["created"]


# ======== Bills Model ========
class Bill(models.Model):
    bill = models.CharField(max_length=100)
    due_date = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(31)]
    )
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.bill} bill due on day({self.due_date}) of the month"

    class Meta:
        ordering = ["-due_date"]
