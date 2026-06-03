import os
import tomllib
from pathlib import Path

from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render


def home(request):
    pyproject_path = Path(__file__).resolve().parent.parent / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        version = tomllib.load(f)["project"]["version"]

    env = os.environ.get("WINGS_ENV", "local")

    return render(request, "home.html", {"version": version, "env": env})


def healthz(request):
    return JsonResponse({"status": "ok"})


def healthz_ready(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "ready"})
    except Exception as exc:
        return JsonResponse({"status": "not ready", "error": str(exc)}, status=503)
