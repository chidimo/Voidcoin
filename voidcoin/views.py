from pathlib import Path
from django.shortcuts import render
from django.conf import settings

def read_me(request):
    template = 'readme.html'

    with open(Path().joinpath(settings.BASE_DIR, "README.md")) as f:
        text = f.read()
        print(text)
    return render(request, template, {"text": text})
