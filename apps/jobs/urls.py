from django.urls import path
from apps.jobs import views

app_name = "jobs"

urlpatterns = [
    path("", views.job_list, name="list"),
    path("create/", views.create_job, name="create"),
    path("<uuid:id>/delete", views.delete_job, name="delete"),
    path("<uuid:id>/", views.detail_job, name="detail"),
    path("edit/<uuid:id>", views.edit_job, name="edit"),
    path("<uuid:id>/apply", views.apply_job, name="apply"),
    path("<uuid:id>/save", views.save_job, name="save"),
    path("<uuid:id>/unsave", views.unsave_job, name="unsave"),
]