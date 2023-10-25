from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from .forms import StudentRegistrationForm, LecturerRegistrationForm


# Login view
class CustomLoginView(LoginView):
    template_name = 'djangoApp/login.html'
    success_url = 'home'


# Registration view for students
def student_registration(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_student = True  # Set the 'is_student' field to True
            user.save()
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'djangoApp/student_registration.html', {'form': form})


# Registration view for lecturers
def lecturer_registration(request):
    if request.method == 'POST':
        form = LecturerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_lecturer = True  # Set the 'is_lecturer' field to True
            user.save()
            return redirect('login')
    else:
        form = LecturerRegistrationForm()
    return render(request, 'djangoApp/lecturer_registration.html', {'form': form})


@login_required
def home(request):
    user = request.user
    contex = {'user': user, 'title': 'Home', 'header': 'Home Page'}
    return render(request=request, template_name='djangoApp/home.html', context=contex)
