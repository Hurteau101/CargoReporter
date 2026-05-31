from django.contrib import admin

from awb_scanner.models import AWBScanner

@admin.register(AWBScanner)
class AWBScannerAdmin(admin.ModelAdmin):
    readonly_fields = ['date_added']