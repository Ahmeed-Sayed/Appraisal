from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from .forms import CombinedForm


class HomeView(TemplateView):
    template_name = "accounts/home.html"


class LoginView(View):
    def get(self, request):
        context = {}
        return render(
            request,
            "accounts/login.html",
        )

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                userId = get_object_or_404(User, username=user)
                request.session["userId"] = userId.id
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password")
                return render(request, "accounts/login.html", status=402)
        else:
            messages.error(request, "username or password were not provided")
            return render(
                request,
                "accounts/login.html",
            )


def logoutUser(request):
    request.session.flush()
    return redirect("home")


class CreateUser(View):
    def get(self, request):
        form = CombinedForm()
        return render(request, "accounts/createUser.html", {"form": form})

    def post(self, request):
        form = CombinedForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully")
            return redirect("home")
        else:
            messages.error(request, "User creation failed")
            return render(request, "accounts/createUser.html", {"form": form})
