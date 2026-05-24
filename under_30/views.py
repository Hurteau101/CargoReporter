import json
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from under_30.models import AWBData
from awb_status.models import AWBStatus


class UpdateSentAWB(View):
    def patch(self, request, awb_number):
        body = json.loads(request.body)
        updated = AWBData.objects.filter(awb_number=awb_number).update(sent=body.get("status", False))

        if not updated:
            return JsonResponse({"message": "AWB not found"}, status=404)

        return HttpResponse(status=204)


class TransferAWBView(View):
    def post(self, request):
        body = json.loads(request.body)

        AWBStatus.objects.update_or_create(
            awb_number=body.get("awb_number"),
            defaults={
                'destination_iata': body.get("destination"),
                'consignee': body.get("consignee"),
                'pieces_on_hand': body.get("pieces"),
                'weight_on_hand': body.get("weight"),
                'days_on_hand': body.get("days"),
                'priority': body.get("priority"),
                'description': body.get("description"),
            }
        )

        found_awb = AWBData.objects.filter(awb_number=body.get("awb_number")).exists()
        if found_awb:
            AWBData.objects.filter(awb_number=body.get("awb_number")).update(has_been_transferred=True)

        # deleted, _ = AWBData.objects.filter(awb_number=body.get("awb_number")).delete()
        #
        # if not deleted:
        #     return JsonResponse({"message": "AWB not found"}, status=404)

        return HttpResponse(status=201)


class Under30View(View):
    def get(self, request):
        awbs = AWBData.objects.filter(hours_remaining__lt=30)

        stats = awbs.aggregate(
            total=Count('awb_number'),
            under_6=Count('awb_number', filter=Q(hours_remaining__lt=6)),
            between_6_15=Count('awb_number', filter=Q(hours_remaining__range=[6, 15])),
            between_15_30=Count('awb_number', filter=Q(hours_remaining__range=[16, 30]))
        )



        awb_json = json.dumps([{
            'awb_number': awb.awb_number,
            'destination': awb.destination_iata,
            'consignee': awb.consignee,
            'pieces': awb.pieces_on_hand,
            'weight': float(awb.weight_on_hand),
            'days': awb.days_on_hand,
            'hours': awb.hours_remaining,
            "priority": awb.priority,
            "description": awb.description,
        } for awb in awbs], default=str)


        return render(request, 'under_30.html', context={'stats': stats, "awb_list": awbs, "awb_json": awb_json})

