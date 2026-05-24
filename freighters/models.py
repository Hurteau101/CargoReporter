from django.db import models

class Freighters(models.Model):
    class AircraftTypes(models.TextChoices):
        DASH100 = 'DASH100', 'Dash 100'
        DASH300 = 'DASH300', 'Dash 300'
        METRO = 'METRO', 'Metro'
        OTHER = 'OTHER', 'Other'

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        DELAYED = 'DELAYED', 'Delayed'
        IN_MAINTENANCE = 'IN_MAINTENANCE', 'In Maintenance'
        CANCELLED = 'CANCELLED', 'Cancelled'
        COMPLETED = 'COMPLETED', 'Completed'
        ON_GROUND = 'ON_GROUND', 'On Ground'

    aircraft_type = models.CharField(
        max_length=15,
        choices=AircraftTypes.choices,
    )
    tail_number = models.CharField(max_length=20, blank=False, null=False)
    flight_number = models.CharField(max_length=20, blank=False, null=False)
    departure = models.CharField(max_length=4, blank=False, null=False)
    destination = models.CharField(max_length=4, blank=False, null=False)
    departure_time = models.DateTimeField(blank=False, null=False)
    arrival_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
    )
    notes = models.TextField(blank=True, null=True)
    station_notified = models.BooleanField(default=False)
    station_informed_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Freighters'
        db_table = 'freighters'

    def __str__(self):
        return f'{self.flight_number} - {self.tail_number} - {self.departure_time}'