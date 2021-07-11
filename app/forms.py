from django.forms import ModelForm
from .models import Student, StudentClass


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'


class StudentClassForm(ModelForm):
    class Meta:
        model = StudentClass
        fields = '__all__'
