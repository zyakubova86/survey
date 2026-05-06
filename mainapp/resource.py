from import_export import resources
from .models import Employees, Questions


class EmployeesResource(resources.ModelResource):
    class Meta:
        model = Employees
        fields = ['code', 'name', 'department']


class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question
        fields = ['prompt',]