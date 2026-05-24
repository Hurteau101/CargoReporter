from django.contrib import admin
from under_30.models import AWBData

@admin.register(AWBData)
class AWBDataAdmin(admin.ModelAdmin):
    search_fields = ['awb_number']