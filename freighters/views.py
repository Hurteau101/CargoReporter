import json
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from freighters.forms import FreightersForm
from freighters.models import Freighters

"""
This view is in charge of handling:
- Deleting freighters
- Displaying freighters
- Adding freighters
- Editing freighters
"""

class DeleteFreighterView(View):
    def delete(self, request, freighter_id):
        deleted, _ = Freighters.objects.filter(id=freighter_id).delete()
        if not deleted:
            return JsonResponse({"message": "Freighter not found"}, status=404)

        return JsonResponse({}, status=204)

class AddFreighterView(View):
    def post(self, request):
        form = FreightersForm(request.POST)
        if form.is_valid():
            freighter = form.save()
            return JsonResponse({
                'id': freighter.id,
                'aircraft_type_display': freighter.get_aircraft_type_display(),
                'tail_number': freighter.tail_number,
                'flight_number': freighter.flight_number,
                'departure': freighter.departure,
                'destination': freighter.destination,
                'departure_time': str(freighter.departure_time),
                'arrival_time': str(freighter.arrival_time),
                'status_display': freighter.get_status_display(),
                'status': freighter.status,
                'station_informed_name': freighter.station_informed_name,
                'station_notified': freighter.station_notified,
                'notes': freighter.notes,

            })

        errors = []
        for field, field_errors in form.errors.items():
            for error in field_errors:
                errors.append(f"{field.title()}: {error}")

        return JsonResponse({"errors": errors}, status=400)


class EditFreighterView(View):
    def post(self, request, freighter_id):
        freighter = Freighters.objects.get(id=freighter_id)
        form = FreightersForm(request.POST, instance=freighter, prefix="edit")

        if form.is_valid():
            form.save()
            return JsonResponse({}, status=204)

        errors = []
        for field, field_errors in form.errors.items():
            for error in field_errors:
                errors.append(f"{field.title()}: {error}")

        return JsonResponse({"errors": errors}, status=400)


class FreightersView(View):
    def get(self, request):
        form = FreightersForm()
        edit_form = FreightersForm(prefix="edit")

        freighters = Freighters.objects.all()
        freighter_stats = freighters.aggregate(
            total=Count('id'),
            active=Count('id', filter=Q(status='ACTIVE')),
            in_maintenance=Count('id', filter=Q(status='IN_MAINTENANCE')),
            delayed=Count('id', filter=Q(status='DELAYED')),
            station_notified=Count('id', filter=Q(station_notified=True)),
        )

        freighter_list = list(freighters.values(
            'id',
            'aircraft_type',
            'tail_number',
            'flight_number',
            'departure',
            'destination',
            'departure_time',
            'arrival_time',
            'status',
            'station_informed_name',
            'station_notified',
            'notes',
        ))

        freighter_list = json.dumps(freighter_list, default=str)


        return render(request, "freighters.html", context={
            "form": form,
            "edit_form": edit_form,
            "freighters": freighters,
            "freighter_stats": freighter_stats,
            "freighter_list": freighter_list,
        })