from django.contrib import admin
from under_30.models import AWBUnder30Hours

@admin.register(AWBUnder30Hours)
class AWBDataAdmin(admin.ModelAdmin):
    search_fields = ['awb_number']