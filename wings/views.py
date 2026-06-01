import os
import tomllib
from pathlib import Path

from django.shortcuts import render


def home(request):
    pyproject_path = Path(__file__).resolve().parent.parent / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        version = tomllib.load(f)["project"]["version"]

    env = os.environ.get("WINGS_ENV", "local")

    return render(request, "home.html", {"version": version, "env": env})
