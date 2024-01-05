from django.urls import path

from . import views

urlpatterns = [
    path("submitAP/", views.AppraisalBleuprintSubmitView.as_view(), name="submitAP"),
    path(
        "<int:blueprintID>/submitInstance/",
        views.AppraisalInstanceSubmitView.as_view(),
        name="submitInstance",
    ),
    path("", views.AppraisalList.as_view(), name="appraisalList"),
    path("<blueprintId>/detail", views.appraisalDetail, name="appraisalDetail"),
]
