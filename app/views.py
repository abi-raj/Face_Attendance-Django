from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import StudentForm, StudentClassForm
import cv2

from .mlfunctions import capture_face, get_directories, get_csvs_by_date, get_csv_data
from .models import StudentClass, Student


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="app/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


def index(request):
    # objs = Student.objects.all()
    # objs = list(objs)
    # print(objs)
    # {"students": objs}
    return render(request, "home.html", )


def stu_list(request):
    objs = Student.objects.all()
    objs = list(objs)
    print(objs)
    {"students": objs}
    return render(request, "stulist.html", {"students": objs})


def add_class(request):
    context = {}
    if request.method == 'POST':
        form = StudentClassForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect('/')
    else:
        form = StudentClassForm()
        context['form'] = form
    return render(request, "add.html", {'form': form})


def add_student(request):
    context = {}
    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            regno = form.save()

        return capture_face(request, regno)
    else:
        form = StudentForm()
        context['form'] = form
    return render(request, "add.html", {'form': form})


def dirss(request):
    dirs_list = get_directories()
    return render(request, 'directory.html', {"dirs": dirs_list})


def filess(request, date_input):
    csvs = get_csvs_by_date(date_input)
    return render(request, 'csvfiles.html', csvs)


def csv_data(request, file_name, path):
    data = get_csv_data(file_name, path)
    return render(request, 'attendData.html', {"data": data, "date": file_name.split('.')[0]})
