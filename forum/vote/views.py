from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import CreateProjectForm

from .models import Project, File


def index(request):
    return redirect(to="vote:registration_project")


def home(request):
    return render(request=request,
                  template_name="vote/base.html")


def registration_project(request):
    if request.method == "POST":
        form = CreateProjectForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            try:
                project = Project.objects.create(
                    fio=form.cleaned_data["name"],
                    code=form.cleaned_data["code"],
                    phone=form.cleaned_data["phone"],
                    email=form.cleaned_data["email"],
                    project_name=form.cleaned_data["project_name"],
                    project_description=form.cleaned_data["project_description"]
                )

                files = form.cleaned_data["files"]

                for file in files:
                    File.objects.create(project=project, file=file)

                messages.success(request, 'Проект успешно зарегистрирован.')
                return redirect("vote:registration_project")

            except Exception as e:
                messages.error(request, 'Произошла ошибка при регистрации проекта. Повторите попытку')

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

    context = {
        "projects": projects,
    }
    return render(request=request,
                  template_name="vote/all_project.html",
                  context=context)
