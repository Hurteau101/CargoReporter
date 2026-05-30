from django.db import models


class Destinations(models.TextChoices):
    YBT = 'YBT', 'YBT'
    YCR = 'YCR', 'YCR'
    YVZ = 'YVZ', 'YVZ'
    YGO = 'YGO', 'YGO'
    ZGI = 'ZGI', 'ZGI'
    YIV = 'YIV', 'YIV'
    XLB = 'XLB', 'XLB'
    YYB = 'YYB', 'YYB'
    YNO = 'YNO', 'YNO'
    YNE = 'YNE', 'YNE'
    YOH = 'YOH', 'YOH'
    YPM = 'YPM', 'YPM'
    YRL = 'YRL', 'YRL'
    YRS = 'YRS', 'YRS'
    ZPB = 'ZPB', 'ZPB'
    ZSJ = 'ZSJ', 'ZSJ'
    YAM = 'YAM', 'YAM'
    YXL = 'YXL', 'YXL'
    YSB = 'YSB', 'YSB'
    ZTM = 'ZTM', 'ZTM'
    XSI = 'XSI', 'XSI'
    YST = 'YST', 'YST'
    XTL = 'XTL', 'XTL'
    YTH = 'YTH', 'YTH'
    YQT = 'YQT', 'YQT'
    ZAC = 'ZAC', 'ZAC'
    ZRJ = 'ZRJ', 'ZRJ'
    YWG = 'YWG', 'YWG'


class AWBScanner(models.Model):
    awb_number = models.CharField(max_length=12, primary_key=True)
    destination_iata = models.CharField(max_length=10, choices=Destinations.choices)
    scan_count = models.IntegerField(default=0)
    scan_time = models.DateTimeField()

    class Meta:
        db_table = 'awb_scanner'
        verbose_name_plural = 'AWB Scanners'

