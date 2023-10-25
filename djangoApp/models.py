# Create your models here.
# models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class AcademicYear(models.Model):
    academic_year = models.CharField(max_length=9, unique=True)  # e.g., "2023-2024"

    def __str__(self):
        return self.academic_year


SEMESTER_CHOICES = (
    ('1', '1'),
    ('2', '2'),
)


class Semester(models.Model):
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES, unique=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

    def __str__(self):
        return self.semester


class Unit(models.Model):
    unit_name = models.CharField(max_length=100, unique=True)
    unit_code = models.CharField(max_length=10, unique=True)
    unit_description = models.CharField(max_length=200, blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('unit_name', 'unit_code')
        ordering = ['semester', 'unit_code', 'unit_name']

    def __str__(self):
        return f"{self.unit_code} ({self.unit_name})"


class Course(models.Model):
    course_name = models.CharField(max_length=100, unique=True)
    course_code = models.CharField(max_length=10, unique=True)
    units = models.ManyToManyField(Unit)
    course_description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.course_name


# Define a custom user manager that can handle different types of users
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        # Create and save a regular user with the given email and password
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        # Create and save a superuser with the given email and password
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(email, password, **extra_fields)

    def create_student(self, student_id, password, **extra_fields):
        # Create and save a student user with the given student_id and password
        extra_fields.setdefault("is_student", True)
        if extra_fields.get("is_student") is not True:
            raise ValueError("Student must have is_student=True")
        return self.create_user(student_id, password, **extra_fields)

    def create_lecturer(self, pf_number, password, **extra_fields):
        # Create and save a lecturer user with the given pf_number and password
        extra_fields.setdefault("is_lecturer", True)
        if extra_fields.get("is_lecturer") is not True:
            raise ValueError("Lecturer must have is_lecturer=True")
        return self.create_user(pf_number, password, **extra_fields)


# Define an abstract base user model that defines the common fields and methods for all users
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# Define a student model that inherits from the base user model and adds student-specific fields and methods
class Student(CustomUser):
    # Basic student information
    student_id = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15)

    # Enrolled units (many-to-many relationship with Unit model)
    enrolled_units = models.ManyToManyField(Unit)

    USERNAME_FIELD = "student_id"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.student_id})"


# Define a lecturer model that inherits from the base user model and adds lecturer-specific fields and methods
class Lecturer(CustomUser):
    pf_number = models.CharField(max_length=10, unique=True)
    units = models.ManyToManyField(Unit)

    USERNAME_FIELD = "pf_number"
    REQUIRED_FIELDS = ["email", "firstname", "lastname"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} (PF: {self.pf_number})"
