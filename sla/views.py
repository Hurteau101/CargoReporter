from collections import defaultdict
from django.db.models import Sum
from django.shortcuts import render
from django.views import View
from sla.models import SLA
class SLAView(View):
    def get(self, request):
        sla = SLA.objects.all()
        # sla_destination = sla.values_list('destination_iata', "hours_remaining").distinct()
        sla_weights = sla.values("destination_iata").annotate(
            total_weight=Sum("weight_on_hand")
        ).order_by("-total_weight")

        destinations = defaultdict(list)
        for row in SLA.objects.values():
            destinations[row['destination_iata']].append(row)

        destinations = dict(destinations)

        total_weight = sla.aggregate(Sum('weight_on_hand'))['weight_on_hand__sum']

        return render(request, 'sla.html', context={
            'sla': sla,
            'sla_weights': sla_weights,
            'destinations': destinations,
            'total_weight': total_weight,
        })
