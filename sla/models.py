from django.db import models

from homepage.models import AWBBase


class SLA(AWBBase):
    hours_remaining = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'sla'
        verbose_name_plural = 'SLA'

    def __str__(self):
        return self.awb_number