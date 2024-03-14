from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import CreateProjectForm

from .models import Project, File, Photo


def index(request):
    return redirect(to="vote:home")


def home(request):
    return render(request=request,
                  template_name="vote/base.html")


def registration_project(request):
    if request.method == "POST":
        form = CreateProjectForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            print("form valid")
            try:
                project = Project.objects.create(fio=form.cleaned_data["name"],
                                                 code=form.cleaned_data["code"],
                                                 phone=form.cleaned_data["phone"],
                                                 email=form.cleaned_data["email"],
                                                 project_name=form.cleaned_data["project_name"],
                                                 project_description=form.cleaned_data[
                                                     "project_description"])

                photos = form.cleaned_data["photos"]
                files = form.cleaned_data["files"]
                for photo in photos:
                    Photo.objects.create(project=project,
                                         photo=photo)

                for file in files:
                    File.objects.create(project=project,
                                        file=file)
                messages.success(request, 'Проект успешно зарегистрирован.')
                return redirect("vote:home")

            except Exception as e:
                print(f"{e}")
                messages.error(request, 'Произошла ошибка при регистрации проекта.')
        else:
            print(form.errors)
            messages.error(request=request,
                           message='Пожалуйста, введите корректные данные.')

    else:
        form = CreateProjectForm()
    context = {
        "form": form
    }
    return render(request=request,
                  template_name="vote/registration_project.html",
                  context=context)


def all_project(request):
    projects = Project.objects.all()

    for project in projects:
        project.files = File.objects.filter(project=project)
        project.photos = Photo.objects.filter(project=project)

    context = {
        "projects": projects,
    }
    for obj in projects:
        print(obj.__dict__)

    return render(request=request,
                  template_name="vote/all_project.html",
                  context=context)
