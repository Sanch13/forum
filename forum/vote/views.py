from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt

from .forms import CreateProjectForm

from .models import Project, File


def index(request):
    return redirect(to="vote:registration_project")


def home(request):
    return render(request=request,
                  template_name="vote/base.html")


@csrf_exempt
def upload_files(request):
    if request.method == 'POST' and request.FILES:
        uploaded_files = []
        for file in request.FILES.getlist('files'):
            file_path = default_storage.save(file.name, file)
            uploaded_files.append(file_path)
            print("upload_files", uploaded_files)
            request.session['uploaded_files'] = uploaded_files
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def registration_project(request):
    if request.method == "POST":
        form = CreateProjectForm(data=request.POST)
        if form.is_valid():
            try:
                project = Project.objects.create(
                    fio=form.cleaned_data["fio"],
                    code=form.cleaned_data["code"],
                    phone=form.cleaned_data["phone"],
                    email=form.cleaned_data["email"],
                    project_name=form.cleaned_data["project_name"],
                    main_idea=form.cleaned_data["main_idea"],
                    project_description=form.cleaned_data["project_description"]
                )

                uploaded_files = request.session.pop('uploaded_files', [])

                for file in uploaded_files:
                    File.objects.create(project=project, file=file)

                messages.success(request, 'Проект успешно зарегистрирован.')
                return redirect("vote:registration_project")

            except Exception as e:
                messages.error(request,
                               'Произошла ошибка при регистрации проекта. Повторите попытку')

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
