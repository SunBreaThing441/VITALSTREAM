from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import DonneurRegisterForm, HopitalRegisterForm


def register_donneur(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
            return redirect("dashboard_admin")
        elif hasattr(request.user, "donneur"):
            return redirect("dashboard_donneur")
        elif hasattr(request.user, "hopital"):
            return redirect("dashboard_hopital")

    form = DonneurRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Enrôlement citoyen réussi. Bienvenue sur le réseau VitalStream !")
        return redirect("dashboard_donneur")
    elif request.method == "POST":
        messages.error(request, "Veuillez corriger les anomalies identifiées dans le formulaire d'enrôlement.")

    return render(request, "accounts/register_donneur.html", {"form": form})


def register_hopital(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
            return redirect("dashboard_admin")
        elif hasattr(request.user, "donneur"):
            return redirect("dashboard_donneur")
        elif hasattr(request.user, "hopital"):
            return redirect("dashboard_hopital")

    form = HopitalRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Dépôt d'accréditation réussi. Votre centre est en attente d'homologation UNESCO.")
        return redirect("dashboard_hopital")
    elif request.method == "POST":
        messages.error(request, "Veuillez corriger les anomalies identifiées dans le dossier d'accréditation.")

    return render(request, "accounts/register_hopital.html", {"form": form})


def login_view(request):
    # Guard: If already authenticated, route directly to the designated role dashboard
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
            return redirect("dashboard_admin")
        elif hasattr(request.user, "donneur"):
            return redirect("dashboard_donneur")
        elif hasattr(request.user, "hopital"):
            return redirect("dashboard_hopital")
        else:
            return redirect("index")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Authentification réussie. Session active pour {username}.")

            # Compute intended target or role dashboard
            next_url = request.POST.get("next") or request.GET.get("next")

            if user.is_superuser or user.is_staff:
                role_target = "dashboard_admin"
            elif hasattr(user, "donneur"):
                role_target = "dashboard_donneur"
            elif hasattr(user, "hopital"):
                role_target = "dashboard_hopital"
            else:
                role_target = "index"

            # Check next_url security and authorization
            if next_url and next_url.startswith("/") and not next_url.startswith("//"):
                if "/dashboard/admin/" in next_url:
                    if user.is_superuser or user.is_staff:
                        return redirect(next_url)
                elif "/dashboard/donneur/" in next_url:
                    if hasattr(user, "donneur"):
                        return redirect(next_url)
                elif "/dashboard/hopital/" in next_url:
                    if hasattr(user, "hopital"):
                        return redirect(next_url)

            return redirect(role_target)
        else:
            messages.error(request, "Échec d'authentification : Identifiant ou mot de passe incorrect.")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    messages.info(request, "Session sécurisée terminée. Vous avez été déconnecté du réseau VitalStream.")
    return redirect("login")
