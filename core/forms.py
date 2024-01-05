from django.core.exceptions import ValidationError
from django import forms
from core.models import (
    GroupObjectiveInstance,
    ObjectivePerspectiveBlueprint,
    InstanceNotes,
    GroupObjective,
)
from django.utils import timezone


# class AppraisalForm(forms.ModelForm):
#     class Meta:
#         model = Appraisal
#         fields = [
#             "object",
#             "description",
#             "targetDate",
#             "actualDate",
#             "weight",
#             "kpis",
#         ]
#         labels = {
#             "object": "Objectives Prespective",
#             "description": "Description",
#             "targetDate": "Target Date",
#             "actualDate": "Actual Date",
#             "kpis": "Measure/KPIs",
#             "weight": "Weight",
#         }


#         widgets = {
#             "object": forms.Select(attrs={"class": "form-select"}),
#             "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
#             "targetDate": forms.DateInput(
#                 attrs={"class": "form-control", "type": "date"}
#             ),
#             "actualDate": forms.DateInput(
#                 attrs={"class": "form-control", "type": "date"}
#             ),
#             "weight": forms.TextInput(attrs={"class": "form-control"}),
#             "kpis": forms.TextInput(attrs={"class": "form-control"}),
#         }
#     def __init__(self, *args, **kwargs):
#         super(AppraisalForm, self).__init__(*args, **kwargs)
#         self.label_suffix = ''
#     def clean(self):
#         cleaned_data = super().clean()
#         targetDate = cleaned_data.get("targetDate")

#         if targetDate < timezone.now().date():
#             raise ValidationError("Target date cannot be in the past.")

#         return cleaned_data


class AppraisalBlueprintSubmitForm(forms.ModelForm):
    class Meta:
        model = ObjectivePerspectiveBlueprint
        fields = [
            "objectivePerspective",
            "groupObjective",
            "objectiveDescription",
            "kpiMeasure",
            "monitoringFrequency",
            "targetDate",
            "weight",
            "target",
        ]
        labels = {
            "objectivePerspective": "Objective Perspective",
            "groupObjective": "Group Objective",
            "objectiveDescription": "Objective Description",
            "kpiMeasure": "KPI/Measure",
            "weight": "Weight",
            "target": "Target",
            "targetDate": "Target Date",
            "monitoringFrequency": "Monitoring Frequency",
        }

        widgets = {
            "targetDate": forms.DateInput(attrs={"type": "date"}),
            "objectiveDescription": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "kpiMeasure": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(AppraisalBlueprintSubmitForm, self).__init__(*args, **kwargs)
        self.fields["groupObjective"].queryset = GroupObjective.objects.filter(
            department=user.department
        )
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
        self.label_suffix = ""

    def clean(self):
        cleaned_data = super().clean()
        targetDate = cleaned_data.get("targetDate")

        if targetDate < timezone.now().date():
            raise ValidationError("Target date cannot be in the past.")

        return cleaned_data


class GroupObjectiveInstanceForm(forms.ModelForm):
    class Meta:
        model = GroupObjectiveInstance
        fields = [
            "evidence",
            "file",
            "actualDate",
        ]
        labels = {"evidence": "Evidence", "actualDate": "Actual Date", "file": ""}
        widgets = {
            "actualDate": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "evidence": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "file": forms.FileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(GroupObjectiveInstanceForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

        self.label_suffix = ""


class NoteForm(forms.ModelForm):
    class Meta:
        model = InstanceNotes
        fields = [
            "text",
        ]
        labels = {"text": "Note"}
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields["text"].widget.attrs.update(
            {
                "class": "form-control",
            }
        )
        self.label_suffix = ""


class groupObjectiveSubmitForm(forms.ModelForm):
    class Meta:
        model = GroupObjective
        fields = ["objectivePerspective", "name", "weight"]
        labels = {
            "name": "Group Objective Name",
            "objectivePerspective": "Objective Perspective",
            "weight": "Weight",
        }
        widgets = {
            "objectivePerspective": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "weight": forms.TextInput(attrs={"class": "form-control"}),
        }
        label_suffix = ""
