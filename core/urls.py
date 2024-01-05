from django.urls import path

from . import views

urlpatterns = [
    path(
        "submit-appraisal/",
        views.AppraisalBleuprintSubmitView.as_view(),
        name="submit-appraisal",
    ),
    path(
        "<int:blueprintID>/submitInstance/",
        views.AppraisalInstanceSubmitView.as_view(),
        name="submit-instance",
    ),
    path("", views.AppraisalList.as_view(), name="appraisal-list"),
    path("<blueprintId>/detail", views.appraisalDetail, name="appraisal-details"),
    path(
        "submit-group-objective", views.SubmitGroupObjective.as_view(), name="submit-group-objective"
    ),
]
