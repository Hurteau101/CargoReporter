from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from freighters.forms import FreightersForm
from freighters.models import Freighters




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

class FreightersView(View):
    def get(self, request):
        form = FreightersForm()

        freighters = Freighters.objects.all()
        freighter_stats = freighters.aggregate(
            total=Count('id'),
            active=Count('id', filter=Q(status='ACTIVE')),
            in_maintenance=Count('id', filter=Q(status='IN_MAINTENANCE')),
            delayed=Count('id', filter=Q(status='DELAYED')),
            station_notified=Count('id', filter=Q(station_notified=True)),
        )


        return render(request, "freighters.html", context={
            "form": form,
            "freighters": freighters,
            "freighter_stats": freighter_stats,
        })