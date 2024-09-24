from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ["student", "date"]
    
    def __str__(self):
        return f"{self.student.name} - {self.date} - {"Present" if self.present else "Absent"}"
