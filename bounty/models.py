from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class WantedCriminal(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)  # real name, may be unknown
    nickname = models.CharField(max_length=200)
    reward = models.PositiveIntegerField()

    # Last known location: coordinates and/or a text note
    latitude = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitude = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )
    location_note = models.TextField(blank=True, default='')

    difficulty = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    armed = models.BooleanField(default=False)
    has_crew = models.BooleanField(default=False)
    escape_master = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(difficulty__gte=1, difficulty__lte=10),
                name='difficulty_1_to_10',
            ),
        ]

    def __str__(self):
        return self.nickname


class HuntLog(models.Model):
    criminal = models.ForeignKey(
        WantedCriminal, on_delete=models.CASCADE, related_name='hunts',
    )
    success = models.BooleanField(default=False)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Hunt #{self.id} on {self.criminal}'
