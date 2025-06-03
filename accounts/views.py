from django.contrib.auth import views as auth_views
from django.shortcuts import render
from .forms import CustomerSignUpForm


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"


def signup(request):
    form = CustomerSignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return render(request, "accounts/pending.html")
    return render(request, "accounts/signup.html", {"form": form})
