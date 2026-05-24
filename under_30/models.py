from django.db import models

from homepage.models import AWBBase


class AWBUnder30Hours(AWBBase):
    sent = models.BooleanField(default=False)
    hours_remaining = models.IntegerField(null=True, blank=True)
    has_been_transferred = models.BooleanField(default=False)

    class Meta:
        db_table = 'awb_under_30_hours'
        verbose_name_plural = 'AWB Under 30 Hours'

    def __str__(self):
        return self.awb_number