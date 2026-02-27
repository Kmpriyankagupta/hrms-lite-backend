from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Employee, Attendance
from .serializers import EmployeeSerializer, AttendanceSerializer


def error_response(message, status_code=status.HTTP_400_BAD_REQUEST):
    """Return JSON with 'message' key for frontend."""
    return Response({'message': message}, status=status_code)


class EmployeeListCreateView(APIView):
    """GET list of employees, POST create employee."""

    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        errors = serializer.errors
        if isinstance(errors, dict):
            first = next(iter(errors.values()), None)
            if isinstance(first, list):
                message = first[0] if first else 'Invalid input'
            else:
                message = str(first) if first else 'Invalid input'
        else:
            message = 'Invalid input'
        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetailView(APIView):
    """GET, DELETE employee by id (UUID)."""

    def get_object(self, pk):
        return get_object_or_404(Employee, pk=pk)

    def get(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def delete(self, request, pk):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AttendanceListCreateView(APIView):
    """GET list filtered by employeeId query param, POST create attendance."""

    def get(self, request):
        employee_id = request.query_params.get('employeeId', '').strip()
        if not employee_id:
            return Response([])
        try:
            employee = Employee.objects.get(employee_id=employee_id)
        except Employee.DoesNotExist:
            return Response([])
        records = Attendance.objects.filter(employee=employee)
        serializer = AttendanceSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
        if 'employeeId' in data and 'employee_id' not in data:
            data['employee_id'] = data.get('employeeId', '')
        serializer = AttendanceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        errors = serializer.errors
        if isinstance(errors, dict):
            first = next(iter(errors.values()), None)
            if isinstance(first, list):
                message = first[0] if first else 'Invalid input'
            else:
                message = str(first) if first else 'Invalid input'
        else:
            message = 'Invalid input'
        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
