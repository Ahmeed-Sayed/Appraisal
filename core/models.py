from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import DepartmentManager, DirectHead, Employee,Department

User = get_user_model()

Objective_PERSPECTIVE_CHOICES = [
    ("Financial", "Financial"),
    ("Customer", "Customer"),
    ("Process Improvement", "Process Improvement"),
    ("People", "People"),
]

STATUS_CHOICES = [
    ("open", "Open"),
    ("closed", "Closed"),
]

MONITORING_FREQUENCY_CHOICES = [
    ("Yearly", "Yearly"),
    ("Quarterly", "Quarterly"),
    ("Monthly", "Monthly"),
]


class GroupObjective(models.Model):
    name = models.CharField(max_length=255)
    objectivePerspective = models.CharField(
        max_length=255, choices=Objective_PERSPECTIVE_CHOICES
    )
    weight = models.FloatField()
    department=models.ForeignKey(Department,on_delete=models.CASCADE,related_name='groupObjective')
    def __str__(self):
        return self.name


class GroupObjectiveInstance(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        related_name="groubObjectiveInstance",
    )
    actualDate = models.DateField()
    evidence = models.TextField(max_length=500)
    file = models.FileField(upload_to="evidence/")

    directHeadReview = models.BooleanField(default=False)
    departmentManagerReview = models.BooleanField(default=False)
    hrReview = models.BooleanField(default=False)
    creationDate = models.DateField(default=timezone.now)


class ObjectivePerspectiveBlueprint(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, related_name="Blueprint"
    )

    groupObjective = models.ForeignKey(
        GroupObjective, on_delete=models.SET_NULL, null=True, related_name="blueprint"
    )
    objectivePerspective = models.CharField(
        max_length=255, choices=Objective_PERSPECTIVE_CHOICES
    )
    target = models.IntegerField(blank=True, null=True)
    targetDate = models.DateField(blank=True, null=True)
    monitoringFrequency = models.CharField(
        max_length=255, choices=MONITORING_FREQUENCY_CHOICES
    )
    objectiveDescription = models.TextField()
    kpiMeasure = models.TextField()
    weight = models.FloatField()
    instanceCount = models.IntegerField(default=0, blank=True, null=True)
    totalInstances = models.IntegerField(default=0, blank=True, null=True)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default="open")
    creationDate = models.DateField(default=timezone.now)


class BlueprintObjectiveInstance(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        related_name="BlueprintInstance",
    )
    blueprint = models.ForeignKey(
        ObjectivePerspectiveBlueprint,
        on_delete=models.CASCADE,
        null=True,
        related_name="BlueprintInstance",
    )

    objectiveInstance = models.ForeignKey(
        GroupObjectiveInstance,
        on_delete=models.CASCADE,
        null=True,
        related_name="BlueprintInstance",
    )


class InstanceNotes(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="instanceNote"
    )
    groubObjectiveInstance = models.ForeignKey(
        GroupObjectiveInstance, on_delete=models.CASCADE, related_name="note"
    )
    text = models.CharField(max_length=500, null=True)
