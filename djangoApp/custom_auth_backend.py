# custom_auth_backend

from django.contrib.auth.backends import ModelBackend

from .models import Student, Lecturer


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Attempt to get a student with the provided student ID
            student = Student.objects.get(student_id=username)
            if student.check_password(password):
                return student
        except Student.DoesNotExist:
            try:
                # Attempt to get a lecturer with the provided PF number
                lecturer = Lecturer.objects.get(pf_number=username)
                if lecturer.check_password(password):
                    return lecturer
            except Lecturer.DoesNotExist:
                # Neither a student nor a lecturer with the provided credentials
                return None

    def get_user(self, user_id):
        try:
            return Student.objects.get(pk=user_id)
        except Student.DoesNotExist:
            try:
                return Lecturer.objects.get(pk=user_id)
            except Lecturer.DoesNotExist:
                return None
