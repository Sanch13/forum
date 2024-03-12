from django.shortcuts import render, redirect

from vote.forms import CreateProjectForm


def index(request):
    return redirect(to="vote:home")


def home(request):
    return render(request=request,
                  template_name="vote/base.html")


def registration_project(request):
    form = CreateProjectForm()
    context = {
        "form": form
    }
    return render(request=request,
                  template_name="vote/registration_project.html",
                  context=context)
