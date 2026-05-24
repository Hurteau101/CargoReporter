from django.shortcuts import render
from django.views import View

from awb_status.models import AWBStatus


class AWBStatusView(View):
    def get(self, request):
        awb_status = AWBStatus.objects.all()


        return render(request, 'awb_status.html', context={'awb_status': awb_status})