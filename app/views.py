from django.shortcuts import render, redirect
import calendar
from django.db import IntegrityError
from datetime import datetime
from .models import Student, Attendance


def calendar_view(request):
    today = datetime.today()
    year = today.year
    month = today.month
    cal = calendar.Calendar()
    month = [day for day in cal.itermonthdays(year, month) if day != 0]
    context = {"month": month, "today": today}
    return render(request, "calendar.html", context)


def attendance_view(request, year, month, day):
    selected_date = datetime(year, month, day)
    students = Student.objects.all()

    if request.method == "POST":
        for student in students:
            status = request.POST.get(f"status_{student.id}")
            present = status == "present"
            try:
                attendance, created = Attendance.objects.get_or_create(
                    student=student, date=selected_date, defaults={"present": present}
                )
                if not created:
                    attendance.present = present
                    attendance.save()
            except IntegrityError:
                pass

        return redirect("attendance", year=year, month=month, day=day)

    students_attendance = []
    for student in students:
        attendance = Attendance.objects.filter(
            student=student, date=selected_date
        ).first()
        students_attendance.append(
            {
                "student": student,
                "present": (attendance.present if attendance else None),
            }
        )

    context = {
        "selected_date": selected_date,
        "students_attendance": students_attendance,
    }
    return render(request, "attendance.html", context)


def student_view(request, student_id):
    today = datetime.today()
    year = today.year
    month = today.month
    cal = calendar.Calendar()
    month_days = [day for day in cal.itermonthdays(year, month) if day != 0]
    student = Student.objects.get(id=student_id)
    attended_days = Attendance.objects.filter(
        student_id=student_id, date__year=year, date__month=month, present=True
    ).values_list("date__day", flat=True)

    context = {
        "name": student.name,
        "month": month_days,
        "today": today,
        "attended_days": list(attended_days),
    }
    return render(request, "student.html", context)
