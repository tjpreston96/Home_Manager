from django.forms import ModelForm, Textarea
from .models import Maintenance, Note


class MaintenanceForm(ModelForm):
    class Meta:
        model = Maintenance
        fields = ["date", "nutrients"]


class NoteForm(ModelForm):
    class Meta:
        model = Note
        widgets = {
            "note": Textarea(attrs={"rows": 20}),
        }
        fields = "__all__"
        readonly_fields = ["updated", "timestamp"]


# attrs={"rows": 5, "cols": 20}
