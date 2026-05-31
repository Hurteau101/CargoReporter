from django.db import models


class Destinations(models.TextChoices):
    YGO = 'YGO', 'YGO'
    YIV = 'YIV', 'YIV'
    YOH = 'YOH', 'YOH'
    YST = 'YST', 'YST',
    WGK = 'WGK', 'WGK'
    # ZGI = 'ZGI', 'ZGI'
    # YBT = 'YBT', 'YBT'
    # YCR = 'YCR', 'YCR'
    # YVZ = 'YVZ', 'YVZ'
    # XLB = 'XLB', 'XLB'
    # YYB = 'YYB', 'YYB'
    # YNO = 'YNO', 'YNO'
    # YNE = 'YNE', 'YNE'
    # YPM = 'YPM', 'YPM'
    # YRL = 'YRL', 'YRL'
    # YRS = 'YRS', 'YRS'
    # ZPB = 'ZPB', 'ZPB'
    # ZSJ = 'ZSJ', 'ZSJ'
    # YAM = 'YAM', 'YAM'
    # YXL = 'YXL', 'YXL'
    # YSB = 'YSB', 'YSB'
    # ZTM = 'ZTM', 'ZTM'
    # XSI = 'XSI', 'XSI'
    # XTL = 'XTL', 'XTL'
    # YTH = 'YTH', 'YTH'
    # YQT = 'YQT', 'YQT'
    # ZAC = 'ZAC', 'ZAC'
    # ZRJ = 'ZRJ', 'ZRJ'
    # YWG = 'YWG', 'YWG'


class AWBScanner(models.Model):
    awb_number = models.CharField(max_length=12, primary_key=True)
    destination_iata = models.CharField(max_length=10, choices=Destinations.choices)
    scan_count = models.IntegerField(default=1)
    full_order = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'awb_scanner'
        verbose_name_plural = 'AWB Scanners'

    def __str__(self):
        return self.awb_number
