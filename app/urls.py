from django.urls import path
from .views import calendar_view, attendance_view, student_view

urlpatterns = [
    path("", calendar_view, name="calendar"),
    path(
        "students/<int:year>/<int:month>/<int:day>/",
        attendance_view,
        name="attendance",
    ),
    path("students/<int:student_id>/", student_view, name="student"),
]
