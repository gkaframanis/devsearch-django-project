from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm


def projects(request):
    all_projects = Project.objects.all()
    context = {"projects": all_projects}
    # If we use the app based templates, we need to specify the app folder when we access the template.
    return render(request, "projects/projects.html", context)


def project(request, pk):
    project_obj = Project.objects.get(id=pk)
    return render(request, "projects/single-project.html", {"project": project_obj})


@login_required(login_url="login")
def create_project(request):
    form = ProjectForm()

    if request.method == "POST":
        # request.FILES to get the uploaded files
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("projects")

    context = {"form": form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def update_project(request, pk):
    # We get the project with the specific id (pk)
    project_obj = Project.objects.get(id=pk)
    # We create the form filled with the data of the project_obj
    form = ProjectForm(instance=project_obj)

    if request.method == "POST":
        # We have to also let it know what project we are updating
        form = ProjectForm(request.POST, request.FILES, instance=project_obj)
        if form.is_valid():
            form.save()
            return redirect("projects")

    context = {"form": form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def delete_project(request, pk):
    project_obj = Project.objects.get(id=pk)
    if request.method == "POST":
        project_obj.delete()
        return redirect("projects")
    context = {"object": project_obj}
    return render(request, "projects/delete_template.html", context)

