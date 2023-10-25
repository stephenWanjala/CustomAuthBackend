from django.contrib.auth.forms import UserCreationForm

from .models import Student, Lecturer


class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ['email', 'first_name', 'last_name', 'student_id', 'phone_number']


class LecturerRegistrationForm(UserCreationForm):
    class Meta:
        model = Lecturer
        fields = ['email', 'first_name', 'last_name', 'pf_number',]
