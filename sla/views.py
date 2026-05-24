from django.shortcuts import render
from django.views import View


class SLAView(View):
    def get(self, request):
        return render(request, 'sla.html')
