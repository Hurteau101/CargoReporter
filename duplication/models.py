from django.db import models



class DuplicateAWB(models.Model):
    awb_number = models.CharField(max_length=12, primary_key=True)
    destination_iata = models.CharField(max_length=10)

    class Meta:
        db_table = 'duplicate_awb'
        verbose_name_plural = 'Duplicate AWBs'

    def __str__(self):
        return self.awb_number