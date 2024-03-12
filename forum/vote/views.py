from django.shortcuts import render, redirect


def index(request):
    return redirect(to="vote:home")


def home(request):
    return render(request=request,
                  template_name="vote/base.html")
