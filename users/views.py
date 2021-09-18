from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Skill
from .forms import CustomUserCreationForm, EditProfileForm, SkillForm


# https://docs.djangoproject.com/en/3.2/topics/auth/default/
# https://docs.djangoproject.com/en/3.2/ref/contrib/messages/
def login_user(request):
    page = "login"
    context = {"page": page}
    # It stops the user to go to the login/ page if he is already logged in.
    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist...')

        # Takes the username and password and makes sure that the password matches the username
        # and will either return the User instance or None.
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # login creates a session for this user in the database and add that session to the browser cookies.
            login(request, user)
            return redirect("profiles")
        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, "users/login_register.html", context)


def logout_user(request):
    # To delete the session
    logout(request)
    messages.info(request, 'User was successfully logged out!')
    return redirect("login")


def register_user(request):
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # We hold a temporary instance and we can hold the user instance before processing it.
            user = form.save(commit=False)
            # This we can also take it directly from the form.
            user.username = user.username.lower()
            # SOS: we can see this user to profiles/ thanks to the signal we used to "connect" the User and Profile model.
            user.save()

            messages.success(request, "User account was created!")
            # It's a good practice to log the user immediately after registration.
            login(request, user)
            return redirect("edit-account")

        else:
            messages.error(request, "An error has occurred during registration...")

    context = {"page": page, "form": form}
    return render(request, "users/login_register.html", context)


def profiles(request):
    profiles_all = Profile.objects.all()
    context = {"profiles": profiles_all}
    return render(request, "users/profiles.html", context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)

    top_skills = profile.skill_set.exclude(description__exact="")
    other_skills = profile.skill_set.filter(description="")

    context = {"profile": profile, "top_skills": top_skills, "other_skills": other_skills}
    return render(request, "users/user-profile.html", context)


@login_required(login_url="login")
def user_account(request):
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {"profile": profile, "skills": skills, "projects": projects}
    return render(request, "users/account.html", context)


@login_required(login_url="login")
def edit_account(request):
    profile = request.user.profile
    # We want to prefill the form with the user information.
    form = EditProfileForm(instance=profile)

    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect("account")

    context = {"form": form}

    return render(request, "users/profile_form.html", context)


@login_required(login_url="login")
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)

        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill was added successfully!")
            return redirect("account")

    context = {"form": form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def update_skill(request, pk):
    profile = request.user.profile
    skill = Skill.objects.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)

        if form.is_valid():
            # We already know the owner, because the skill has already been created.
            form.save()
            messages.success(request, "Skill was updated successfully!")
            return redirect("account")

    context = {"form": form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill was deleted successfully!")
        return redirect("account")
    context = {"object": skill}
    return render(request, "delete_template.html", context)
