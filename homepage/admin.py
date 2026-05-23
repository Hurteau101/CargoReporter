from django.contrib import admin

from homepage.models import AWBData, DuplicateAWB

admin.site.register([AWBData, DuplicateAWB])
