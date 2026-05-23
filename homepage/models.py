from django.db import models

class AWBData(models.Model):
    awb_number = models.CharField(max_length=12, primary_key=True)
    destination_iata = models.CharField(max_length=4, blank=False, null=False)
    consignee = models.CharField(max_length=255, blank=False, null=False)
    pieces_on_hand = models.IntegerField(blank=False, null=False)
    weight_on_hand = models.FloatField(blank=False, null=False)
    days_on_hand = models.IntegerField(blank=False, null=False)
    hours_remaining = models.IntegerField(blank=False, null=False)
    sent = models.BooleanField(default=False)
    priority = models.IntegerField(blank=False, null=False)

    class Meta:
        db_table = 'awb_data'
        verbose_name_plural = 'AWB Data'

    def __str__(self):
        return self.awb_number

class DuplicateAWB(models.Model):
    awb_number = models.CharField(max_length=12, primary_key=True)

    class Meta:
        db_table = 'duplicate_awb'
        verbose_name_plural = 'Duplicate AWBs'

    def __str__(self):
        return self.awb_number