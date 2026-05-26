from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from duplication.models import DuplicateAWB

"""
This view is in charge of handling:
- Deleting duplicate AWBs
- Displaying duplicate AWBs
"""

class DeleteDuplicateView(View):
    def delete(self, request, duplicate_awb):
        deleted, _ = DuplicateAWB.objects.filter(awb_number=duplicate_awb).delete()
        if not deleted:
            return JsonResponse({"message": "AWB not found"}, status=404)

        return JsonResponse({}, status=204)

class DuplicateView(View):
    def get(self, request):
        duplicate_awbs = DuplicateAWB.objects.all()

        return render(request, 'duplicates.html', context={'duplicate_awbs': duplicate_awbs})
