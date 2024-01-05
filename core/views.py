from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from accounts.models import Employee
from core.models import BlueprintObjectiveInstance, ObjectivePerspectiveBlueprint
from core.forms import (
    AppraisalBlueprintSubmitForm,
    GroupObjectiveInstanceForm,
    groupObjectiveSubmitForm,
)

from django.contrib.auth import get_user_model

User = get_user_model()

from functools import wraps


def check_user_id_exists(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get("userId") is None:
            return redirect("login")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


class AppraisalBleuprintSubmitView(View):
    @method_decorator(check_user_id_exists)
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.session.get("userId"))
        form = AppraisalBlueprintSubmitForm(user=user)
        return render(request, "core/appraisalSubmit.html", {"form": form})

    @method_decorator(check_user_id_exists)
    def post(self, request, *args, **kwargs):
        form = AppraisalBlueprintSubmitForm(request.POST)
        employee = Employee.objects.get(id=request.session.get("userId"))
        if employee is None:
            return redirect("login")
        if form.is_valid():
            appraisal = form.save(commit=False)
            appraisal.employee = employee
            match form.cleaned_data.get("monitoringFrequency"):
                case "Yearly":
                    appraisal.instanceCount = 1
                case "Quarterly":
                    appraisal.instanceCount = 4
                case "Monthly":
                    appraisal.instanceCount = 12
            appraisal.save()
        return redirect("submit-appraisal")


class AppraisalInstanceSubmitView(View):
    @method_decorator(check_user_id_exists)
    def get(self, request, blueprintID):
        appraisalInstanceForm = GroupObjectiveInstanceForm()
        blueprint = ObjectivePerspectiveBlueprint.objects.get(id=blueprintID)
        context = {
            "appraisalInstanceForm": appraisalInstanceForm,
            "blueprint": blueprint,
        }
        return render(request, "core/appraisalInstanceSubmit.html", context)

    @method_decorator(check_user_id_exists)
    def post(self, request, blueprintID):
        employee = Employee.objects.get(id=request.session["userId"])
        appraisalInstanceForm = GroupObjectiveInstanceForm(request.POST)
        if appraisalInstanceForm.is_valid():
            submittedInstance = appraisalInstanceForm.save(commit=False)
            submittedInstance.employee = employee
            submittedInstance.save()
            blueprint = ObjectivePerspectiveBlueprint.objects.get(id=blueprintID)
            if blueprint.totalInstances is None:
                blueprint.totalInstances = 1
            else:
                blueprint.totalInstances = blueprint.totalInstances + 1
            blueprint.save()
            BlueprintObjectiveInstance.objects.create(
                employee=employee, blueprint=blueprint, objectInstance=submittedInstance
            )
        return redirect("appraisal-list")


class AppraisalList(View):
    @method_decorator(check_user_id_exists)
    def get(self, request, *args, **kwargs):
        userId = request.session.get("userId")
        user = User.objects.get(id=userId)
        blueprints = ObjectivePerspectiveBlueprint.objects.filter(employee=user)
        return render(request, "core/appraisalList.html", {"blueprints": blueprints})


@check_user_id_exists
def appraisalDetail(request, blueprintId):
    if request.method == "GET":
        blueprint = get_object_or_404(ObjectivePerspectiveBlueprint, id=blueprintId)
        blueprintInstances = BlueprintObjectiveInstance.objects.filter(
            blueprint=blueprint
        )
        return render(
            request,
            "core/appraisalDetail.html",
            {"blueprint": blueprint, "blueprintInstances": blueprintInstances},
        )


class SubmitGroupObjective(View):
    @method_decorator(check_user_id_exists)
    def get(self, request, *args, **kwargs):
        form = groupObjectiveSubmitForm()

        return render(request, "core/groupObjectiveSubmit.html", {"form": form})

    @method_decorator(check_user_id_exists)
    def post(self, request, *args, **kwargs):
        userId = request.session.get("userId")
        user = get_object_or_404(User, id=userId)
        form = groupObjectiveSubmitForm(request.POST)
        if form.is_valid():
            submittedForm = form.save(commit=False)
            submittedForm.department = user.department
            submittedForm.save()
            return redirect("appraisal-list")
        return render(request, "core/groupObjectiveSubmit.html", {"form": form})
