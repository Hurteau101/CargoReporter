import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from clients.forms import ClientForm
from clients.models import Clients

"""
This view is in charge of:
- Handling the creation of new clients
- Handling the deletion of clients
- Handling the editing of clients
"""


class DeleteClientView(View):
    def delete(self, request, client_id):
        deleted, _ = Clients.objects.filter(id=client_id).delete()
        if not deleted:
            return JsonResponse({"message": "Client not found"}, status=404)

        return JsonResponse({}, status=204)

class EditClientView(View):
    def post(self, request, client_id):
        client = Clients.objects.get(id=client_id)

        # Add prefix to the form to ensure there are no duplicate HTML IDs and to distinguish between edit and add forms
        form = ClientForm(request.POST, instance=client, prefix="edit")

        if form.is_valid():
            form.save()
            return JsonResponse({}, status=204)

        errors = []
        for field, field_errors in form.errors.items():
            for error in field_errors:
                errors.append(f"{field.title()}: {error}")

        return JsonResponse({"errors": errors}, status=400)

class AddClientView(View):
    def post(self, request):
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            return JsonResponse({
                "id": client.id,
                "company_name": client.company_name,
                "contact_name": client.contact_name,
                "email": client.email,
                "destination": client.destination_iata,
                "notes": client.notes,
            })

        errors = []
        for field, field_errors in form.errors.items():
            for error in field_errors:
                errors.append(f"{field.title()}: {error}")

        return JsonResponse({"errors": errors}, status=400)

class ClientsView(View):
    def get(self, request):
        clients = Clients.objects.all()
        form = ClientForm()

        edit_form = ClientForm(prefix="edit")
        client_list = list(clients.values(
            'id', 'company_name', 'contact_name', 'email', 'destination_iata', 'notes'
        ))

        # JSON format the clients for the frontend to use.
        client_list = json.dumps(client_list, default=str)

        return render(request, 'clients.html', context={
            'form': form,
            'edit_form': edit_form,
            "clients": clients,
            "number_of_clients": len(clients),
            "client_list": client_list,
        })