from django import forms
from clients.models import Clients


class ClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        exclude = ['id']
        widgets = {
            "company_name": forms.TextInput(attrs={"placeholder": "e.g. XYZ", "id": "company"}),
            "contact_name": forms.TextInput(attrs={"placeholder": "e.g. Jane Doe", "id": "contact-name"}),
            "email": forms.EmailInput(attrs={"placeholder": "e.g JaneDoe@gmail.com", "id": "email"}),
            "destination_iata": forms.TextInput(attrs={"placeholder": "e.g. YYZ", "id": "destination"}),
            'notes': forms.Textarea(
                attrs={'id': 'notes', 'placeholder': 'Any additional notes or information about the client.',
                       'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If there is a prefix attached, loop through all fields, and add the prefix
        # we need this as we use this form twice and need to tell the difference between forms.
        # As well ensure there are no duplicate HTML IDs.
        if self.prefix:
            for field_name in self.fields:
                field = self.fields[field_name]
                current_id = field.widget.attrs.get('id')

                if current_id:
                    field.widget.attrs['id'] = f"{self.prefix}-{current_id}"
