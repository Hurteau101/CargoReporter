import json

from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from awb_scanner.models import Destinations, AWBScanner

class SaveAWBScannerView(View):
    def post(self, request):

        data = json.loads(request.body)

        awb_number = data.get('awb')
        destination = data.get('destination')
        scan_time = data.get('time')

        if not all([awb_number, destination, scan_time]):
            return JsonResponse({'error': 'Could not save AWB'}, status=400)

        try:
            AWBScanner.objects.create(
                destination_iata=destination,
                awb_number=awb_number,
                scan_time=scan_time,
                scan_count=1
            )
        except IntegrityError:
            return JsonResponse({'error': 'AWB already exists'}, status=400)

        return JsonResponse({}, status=200)


class UpdateCountView(View):
    def patch(self, request, awb_number):
        found_awb = AWBScanner.objects.filter(awb_number=awb_number).first()
        if not found_awb:
            return JsonResponse({'error': 'AWB not found'}, status=404)

        found_awb.scan_count += 1
        found_awb.save(update_fields=['scan_count'])

        return JsonResponse({}, status=200)

class RemoveAWBScannerView(View):
    def delete(self, request, awb_number):
        deleted, _ = AWBScanner.objects.filter(awb_number=awb_number).delete()
        if not deleted:
            return JsonResponse({"message": "AWB not found"}, status=404)

        return JsonResponse({}, status=204)

class GetAWBScannerView(View):
    def get(self, request):

        already_scanned = AWBScanner.objects.all().order_by('-scan_time')

        return render(request, 'scanner.html', context={
            'destinations': Destinations.choices,
            'already_scanned': already_scanned
        })