import os
import json
from collections import Counter

from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View

from .forms import SLAUploadForm
import pandas as pd
import re
from homepage.models import AWBData, DuplicateAWB
from datetime import datetime

# WE NEED TO CHECK THAT IT STARTS WITH WPG -- SINCE SOMETIMES THERE IS THOMPSON


VALID_COLUMN_HEADERS = {
    'awb date', 'awb no.', 'pcs rcvd', 'wgt rcvd', 'pcs on hand', 'wgt on hand', 'consignee', 'goods', 'remarks',
     'skid', 'pri', 'checked'
}

def _read_file(file) -> pd.DataFrame:
    """
    Reads the file and returns a pandas dataframe
    :param file: File object
    :return: Returns a pandas dataframe
    """
    if file.name.endswith('.csv'):
        return pd.read_csv(file, header=1)

    return pd.read_excel(file, header=1)

def _extract_data(awb_data: dict):
    awb_data_rows = []

    for destination, information in awb_data.items():
        for awb_information in information:
            sla, priority = awb_information["PRI"].split(" ")

            # We want to skip any of these.
            if any([priority is None, sla is None, priority == "NA", sla == "NA"]):
                continue

            awb_created_date = datetime.strptime(awb_information['AWB Date'], "%Y-%m-%d %H:%M").date()
            current_date = datetime.now().date()

            days_on_hand = (current_date - awb_created_date).days

            awb_data_rows.append(AWBData(
                awb_number=awb_information['AWB No.'],
                destination_iata=destination,
                consignee=awb_information['Consignee'],
                pieces_on_hand=awb_information['Pcs On Hand'],
                weight_on_hand=awb_information['Wgt On Hand'],
                days_on_hand=days_on_hand,
                hours_remaining=int(sla),
                priority=int(priority),
            ))

    awb_counts = Counter(row.awb_number for row in awb_data_rows)
    duplicates = [awb for awb, count in awb_counts.items() if count > 1]

    AWBData.objects.bulk_create(
        awb_data_rows,
        update_conflicts=True,
        unique_fields=['awb_number'],
        update_fields=['consignee', 'pieces_on_hand', 'weight_on_hand', 'destination_iata']
    )

    DuplicateAWB.objects.bulk_create([DuplicateAWB(awb_number=awb) for awb in duplicates], batch_size=300, ignore_conflicts=True)


def extract_destination(value) -> str | None:
    """
    Check if it's a destination and return the destination code
    :param value: Value to check
    :return: Returns the destination code if it is a destination else None
    """
    if pd.isna(value) or not value:
        return None

    match = re.search(r'([A-Z0-9]{3,4})\s*=\s*([A-Z0-9]{3,4})$', str(value).strip())
    departure = match.group(1) if match else None

    # Return N/A as we will filter these out. Since these are ones not out of WPG.
    if departure and departure.upper() != "WPG":
        return "N/A"

    # Return the destination code
    return match.group(2) if match else None


def clean_group_data(df: pd.DataFrame) -> dict:
    """
    Group the data by destination
    :param df: Pandas dataframe
    :return: Returns a dictionary of destination and data
    """
    # Forward fill the destination code down to all rows below it
    df['dest'] = df['AWB Date'].apply(extract_destination).ffill()

    # Filter out the N/A values and any rows that don't have a AWB No.
    df = df[(df['AWB No.'].notna()) & (df['dest'] != "N/A")]

    return {dest: group.drop(columns='dest').to_dict('records') for dest, group in df.groupby('dest')}


class ClearDeleteView(View):
    def delete(self, request):
        model_mapper = {
            "duplicate_awbs": DuplicateAWB,
            "sla": AWBData,
        }

        body = json.loads(request.body)

        model_instance = model_mapper.get(body.get("tab_type", None))
        if not model_instance:
            return JsonResponse(
                status=400,
                data=json.dumps({"message": "Invalid Delete Type"})
            )

        model_instance.objects.all().delete()
        return JsonResponse(status=200, data={})

class HomeView(View):
    template_name = 'homepage.html'

    def get(self, request):
        tabs = {
            "SLA Tab": {
                "description": "Removes all SLA data",
                "data_event_name": "sla"
            },
            "Freighters": {
                "description": "Removes all freighter data",
                "data_event_name": "freighters"
            },
            "30 Hour Tab": {
                "description": "Removes all 30 hour data",
                "data_event_name": "30_hours"
            },
            "AWB Status Tab": {
                "description": "Removes all AWB status data",
                "data_event_name": "awb_status"
            },
            "Duplicate AWBs": {
                "description": "Removes all duplicate AWBs",
                "data_event_name": "duplicate_awbs"
            },
            "Mass Clear": {
                "description": "Mass clears all data",
                "data_event_name": "mass_clear"
            }
        }

        return render(request, self.template_name, {
            'form': SLAUploadForm(),
            'tabs': tabs
        })

    def post(self, request):
        form = SLAUploadForm(request.POST, request.FILES)

        if not form.is_valid():
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return render(request, self.template_name, {'form': form})

        file = form.cleaned_data['file']
        df = _read_file(file)

        if df.empty:
            messages.error(request, 'No data found in the file')
            return render(request, self.template_name, {'form': form})

        if not VALID_COLUMN_HEADERS.issubset(set(df.columns.str.lower())):
            messages.error(request, 'Invalid column headers')
            return render(request, self.template_name, {'form': form})

        awb_data = clean_group_data(df)
        _extract_data(awb_data)

        return render(request, self.template_name, {'form': form})
