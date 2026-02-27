import uuid
from django.db import models


class Employee(models.Model):
    """Employee record. employee_id is the unique business identifier."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_id = models.CharField(max_length=64, unique=True, db_index=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    department = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return f"{self.employee_id} - {self.full_name}"


class Attendance(models.Model):
    """Daily attendance record per employee."""
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(fields=['employee', 'date'], name='unique_employee_date')
        ]

    def __str__(self):
        return f"{self.employee.employee_id} - {self.date} - {self.status}"
