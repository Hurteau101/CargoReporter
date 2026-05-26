from django import forms
from freighters.models import Freighters


class FreightersForm(forms.ModelForm):
    class Meta:
        model = Freighters
        exclude = ['id']
        widgets = {
            'aircraft_type': forms.Select(attrs={'id': 'aircraft-type'}),
            'tail_number': forms.TextInput(attrs={'id': 'tail-number', 'placeholder': 'e.g. C-GABC'}),
            'flight_number': forms.TextInput(attrs={'id': 'flight-number', 'placeholder': 'e.g. FX1042'}),
            'departure': forms.TextInput(attrs={'id': 'departure', 'placeholder': 'e.g. YWG'}),
            'destination': forms.TextInput(attrs={'id': 'destination', 'placeholder': 'e.g YYZ'}),
            'departure_time': forms.DateTimeInput(attrs={'id': 'departure-time', 'type': 'datetime-local'}),
            'arrival_time': forms.DateTimeInput(attrs={'id': 'arrival-time', 'type': 'datetime-local'}),
            'status': forms.Select(attrs={'id': 'status'}),
            'station_notified': forms.CheckboxInput(attrs={'id': 'station-notified'}),
            'station_informed_name': forms.TextInput(attrs={'id': 'station-informed-name'}),
            'notes': forms.Textarea(attrs={'id': 'notes', 'placeholder': 'Any additional notes or information about the freighter.', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove the default empty choice and replace it with '-- Select --'
        self.fields['aircraft_type'].choices = [('', '— Select —')] + list(self.fields['aircraft_type'].choices)[1:]
        self.fields['status'].choices = [('', '— Select —')] + list(self.fields['status'].choices)[1:]

        # If there is a prefix attached, loop through all fields, and add the prefix
        # we need this as we use this form twice and need to tell the difference between forms.
        # As well ensure there are no duplicate HTML IDs.
        if self.prefix:
            for field_name in self.fields:
                field = self.fields[field_name]
                current_id = field.widget.attrs.get('id')

                if current_id:
                    field.widget.attrs['id'] = f"{self.prefix}-{current_id}"



