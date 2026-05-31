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
        full_order = data.get('full_order')


        if not all([awb_number, destination, full_order is not None]):
            return JsonResponse({'error': 'Could not save AWB'}, status=400)

        try:
            AWBScanner.objects.create(
                destination_iata=destination,
                awb_number=awb_number,
                full_order=full_order,
            )
        except IntegrityError:
            return JsonResponse({'error': 'AWB already exists'}, status=400)

        return JsonResponse({}, status=200)


class UpdateCountView(View):
    def patch(self, request, awb_number):
        body = json.loads(request.body)
        full_order = body.get('full_order', False)

        found_awb = AWBScanner.objects.filter(awb_number=awb_number).first()
        if not found_awb:
            return JsonResponse({'error': 'AWB not found'}, status=404)

        found_awb.scan_count += 1
        found_awb.full_order = full_order
        found_awb.save(update_fields=['scan_count', 'full_order'])

        return JsonResponse({}, status=200)

class RemoveAWBScannerView(View):
    def delete(self, request, awb_number):
        deleted, _ = AWBScanner.objects.filter(awb_number=awb_number).delete()
        if not deleted:
            return JsonResponse({"message": "AWB not found"}, status=404)

        return JsonResponse({}, status=204)

class GetAWBScannerView(View):
    def get(self, request):

        awbs = AWBScanner.objects.all().order_by('date_added')

        grouped_destinations = {}

        for awb in awbs:
            grouped_destinations.setdefault(awb.destination_iata, []).append({
                "awb_number": awb.awb_number,
                "destination": awb.destination_iata,
                "scan_count": awb.scan_count,
                "full_order": awb.full_order,
            })

        return render(request, 'scanner.html', context={
            'destinations': Destinations.choices,
            'grouped_data': json.dumps(grouped_destinations),
        })