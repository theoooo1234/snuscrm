from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from .forms import CustomerSignUpForm


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"


def signup(request):
    if request.method == "POST":
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "accounts/pending.html")
    else:
        form = CustomerSignUpForm()
    return render(request, "accounts/signup.html", {"form": form})
