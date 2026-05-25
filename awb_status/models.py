from django.db import models
from homepage.models import AWBBase


class AWBStatus(AWBBase):
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'AWB Status'
        db_table = 'awb_status'

    def __str__(self):
        return self.awb_number

