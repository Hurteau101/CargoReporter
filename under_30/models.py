from django.db import models

from homepage.models import AWBBase


class AWBData(AWBBase):
    sent = models.BooleanField(default=False)
    hours_remaining = models.IntegerField(null=True, blank=True)
    has_been_transferred = models.BooleanField(default=False)

    class Meta:
        db_table = 'awb_data'
        verbose_name_plural = 'AWB Data'

    def __str__(self):
        return self.awb_number