import re
from rest_framework import serializers
from .models import Employee, Attendance


EMAIL_REGEX = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee. Exposes employeeId, fullName, email, department for frontend."""
    employeeId = serializers.CharField(source='employee_id', max_length=64)
    fullName = serializers.CharField(source='full_name', max_length=255)
    email = serializers.EmailField()
    department = serializers.CharField(max_length=255)

    class Meta:
        model = Employee
        fields = ['id', 'employeeId', 'fullName', 'email', 'department']
        read_only_fields = ['id']

    def validate_employeeId(self, value):
        value = (value or '').strip()
        if not value:
            raise serializers.ValidationError('Employee ID is required.')
        return value

    def validate_fullName(self, value):
        value = (value or '').strip()
        if not value:
            raise serializers.ValidationError('Full name is required.')
        return value

    def validate_email(self, value):
        value = (value or '').strip().lower()
        if not value:
            raise serializers.ValidationError('Email address is required.')
        if not EMAIL_REGEX.match(value):
            raise serializers.ValidationError('Please enter a valid email address.')
        return value

    def validate_department(self, value):
        value = (value or '').strip()
        if not value:
            raise serializers.ValidationError('Department is required.')
        return value

    def validate(self, attrs):
        employee_id = attrs.get('employee_id') or (self.initial_data.get('employeeId') or '').strip()
        if not employee_id:
            return attrs
        qs = Employee.objects.filter(employee_id__iexact=employee_id)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError({
                'employeeId': 'An employee with this Employee ID already exists.'
            })
        return attrs


class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer for Attendance. Frontend sends employeeId, date, status."""
    employeeId = serializers.CharField(source='employee.employee_id', read_only=True)
    employee_id = serializers.CharField(write_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'employeeId', 'date', 'status', 'employee_id']
        read_only_fields = ['id', 'employeeId']

    def validate_employee_id(self, value):
        value = (value or '').strip()
        if not value:
            raise serializers.ValidationError('Employee is required.')
        if not Employee.objects.filter(employee_id=value).exists():
            raise serializers.ValidationError('Employee not found.')
        return value

    def validate_date(self, value):
        if not value:
            raise serializers.ValidationError('Date is required.')
        return value

    def validate_status(self, value):
        if value not in ('Present', 'Absent'):
            raise serializers.ValidationError('Status must be Present or Absent.')
        return value

    def create(self, validated_data):
        emp_id = validated_data.pop('employee_id')
        employee = Employee.objects.get(employee_id=emp_id)
        attendance, created = Attendance.objects.update_or_create(
            employee=employee,
            date=validated_data['date'],
            defaults={'status': validated_data['status']}
        )
        return attendance
