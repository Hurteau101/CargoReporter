from django import forms


# Use regular form here, as we don't need to store the file. We are more so using it as a form, for upload and
# will extract the data and store into models.
class SLAUploadForm(forms.Form):
    file = forms.FileField(
        widget=forms.FileInput(attrs={
            "id": "sla-file",
            "accept": ".xlsx,.xls,.csv",
        })
    )

    def clean_file(self):
        file = self.cleaned_data["file"]

        if not file.name.lower().endswith((".xlsx", ".xls", ".csv")):
            raise forms.ValidationError("Only Excel or CSV files are allowed.")

        return file




