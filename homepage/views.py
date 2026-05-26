import os
import json
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from duplication.models import DuplicateAWB
from sla.models import SLA
from freighters.models import Freighters
from awb_status.models import AWBStatus
from .forms import SLAUploadForm
import pandas as pd
import re
from under_30.models import AWBUnder30Hours
from datetime import datetime
import cloudinary
import cloudinary.uploader

"""
This view is in charge of:
- Handling the upload of SLA data
- Deleting different types of data
"""

# Set the cloudinary configuration
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET"),
)

# Valid column headers that need to be in the excel file.
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
    """
    Extracts the awb data and saves it to the database
    :param awb_data: Dictionary of grouped awb data.
    """
    under_30_hours_rows = []
    sla_rows = []
    awb_number_list = []
    duplicate_rows = []

    for destination, information in awb_data.items():
        for awb_information in information:
            sla, priority = awb_information["PRI"].split(" ")

            # We want to skip any of these.
            if any([priority is None, sla is None, priority == "NA", sla == "NA"]):
                continue

            awb_created_date = datetime.strptime(awb_information['AWB Date'], "%Y-%m-%d %H:%M").date()
            current_date = datetime.now().date()

            days_on_hand = (current_date - awb_created_date).days

            sla = int(sla)

            awb_number = awb_information['AWB No.'].replace("632-", '')
            awb_number_list.append(awb_number)

            if awb_number_list.count(awb_number) > 1:
                duplicate_rows.append(DuplicateAWB(
                    awb_number=awb_number,
                    destination_iata=destination,
                ))

            if sla <= 30:
                under_30_hours_rows.append(AWBUnder30Hours(
                    awb_number=awb_information['AWB No.'].replace("632-", ''),
                    destination_iata=destination,
                    consignee=awb_information['Consignee'],
                    pieces_on_hand=awb_information['Pcs On Hand'],
                    weight_on_hand=awb_information['Wgt On Hand'],
                    days_on_hand=days_on_hand,
                    hours_remaining=int(sla),
                    priority=int(priority),
                    description=awb_information['Goods'],
                ))

            if sla < 0:
                sla_rows.append(SLA(
                    awb_number=awb_information['AWB No.'].replace("632-", ''),
                    destination_iata=destination,
                    consignee=awb_information['Consignee'],
                    description=awb_information['Goods'],
                    pieces_on_hand=awb_information['Pcs On Hand'],
                    weight_on_hand=awb_information['Wgt On Hand'],
                    days_on_hand=days_on_hand,
                    hours_remaining=int(sla),
                    priority=int(priority),
                ))

    AWBUnder30Hours.objects.bulk_create(
        under_30_hours_rows,
        update_conflicts=True,
        unique_fields=['awb_number'],
        update_fields=['consignee', 'pieces_on_hand', 'weight_on_hand', 'destination_iata']
    )

    SLA.objects.bulk_create(
        sla_rows,
        update_conflicts=True,
        unique_fields=['awb_number'],
        update_fields=['consignee', 'pieces_on_hand', 'weight_on_hand', 'destination_iata']
    )

    DuplicateAWB.objects.bulk_create(
        duplicate_rows,
        update_conflicts=True,
        unique_fields=['awb_number'],
        update_fields=['destination_iata']
    )



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

def _handle_image_delection():
    """Handles the deletion of images from cloudinary."""
    images = [
        image
        for image in AWBStatus.objects.values('image')
    ]

    for image in images:
        if image['image']:
            cloudinary.uploader.destroy(image['image'])

class ClearDeleteView(View):
    def delete(self, request):
        # Map the tab type to the model
        model_mapper = {
            "duplicate_awbs": DuplicateAWB,
            "30_hours": AWBUnder30Hours,
            "awb_status": AWBStatus,
            "freighters": Freighters,
            "sla": SLA,
        }

        body = json.loads(request.body)

        # If the tab type is mass clear, delete all data + images from cloudinary
        if body.get("tab_type", None) == "mass_clear":
            for model in model_mapper.values():
                if model == AWBStatus:
                    _handle_image_delection()

                model.objects.all().delete()

            return JsonResponse(status=200, data={})

        model_instance = model_mapper.get(body.get("tab_type", None))

        if not model_instance:
            return JsonResponse(
                status=400,
                data=json.dumps({"message": "Invalid Delete Type"})
            )

        # If the tab type is AWB Status, delete all images from cloudinary
        if model_instance == AWBStatus:
            _handle_image_delection()

        model_instance.objects.all().delete()
        return JsonResponse(status=200, data={})

class HomeView(View):
    template_name = 'homepage.html'

    def get(self, request):
        sla_exists = SLA.objects.exists()
        freighter_exists = Freighters.objects.exists()
        under_30_exists = AWBUnder30Hours.objects.exists()
        awb_status_exists = AWBStatus.objects.exists()
        duplicate_awb_exists = DuplicateAWB.objects.exists()

        # Creates the different tabs that can be cleared if there is data.
        tabs = {
            "SLA Tab": {
                "description": "Removes all SLA data",
                "data_event_name": "sla",
                "has_data": sla_exists
            },
            "Freighters": {
                "description": "Removes all freighter data",
                "data_event_name": "freighters",
                "has_data": freighter_exists
            },
            "30 Hour Tab": {
                "description": "Removes all 30 hour data",
                "data_event_name": "30_hours",
                "has_data": under_30_exists
            },
            "AWB Status Tab": {
                "description": "Removes all AWB status data",
                "data_event_name": "awb_status",
                "has_data": awb_status_exists
            },
            "Duplicate AWBs": {
                "description": "Removes all duplicate AWBs",
                "data_event_name": "duplicate_awbs",
                "has_data": duplicate_awb_exists
            },
            "Mass Clear": {
                "description": "Mass clears all data",
                "data_event_name": "mass_clear",
                "has_data": any([sla_exists, freighter_exists, under_30_exists, awb_status_exists, duplicate_awb_exists])
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

        return redirect('sla')
