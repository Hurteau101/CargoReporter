from django.db import models

class Clients(models.Model):
    company_name = models.CharField(max_length=255, blank=False, null=False)
    contact_name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    destination_iata = models.CharField(max_length=4, blank=False, null=False,)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'clients'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return self.company_name