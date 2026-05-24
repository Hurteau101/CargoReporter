from django.db import models


# Create an abstract model, so we don't have to re-write the same table data. Both AWBStatus and AWBData can
# reference this table and have the same table columns and validation.
class AWBBase(models.Model):
    awb_number = models.CharField(max_length=12, unique=True)
    destination_iata = models.CharField(max_length=10)
    consignee = models.CharField(max_length=255)
    pieces_on_hand = models.IntegerField(null=True, blank=True)
    weight_on_hand = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    days_on_hand = models.IntegerField(null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True