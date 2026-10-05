from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pypdf import PdfReader
from gtts import gTTS
import os

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm


@login_required
def index(request):
    text = ""

    if request.method == "POST":
        pdf_file = request.FILES["pdf"]
        reader = PdfReader(pdf_file)

        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()

        # Create simple podcast script
        script = "Welcome to today's podcast. Here is a summary of the document. " + text[:1000]

        # Convert to audio
        tts = gTTS(script)
        audio_path = "converter/static/podcast.mp3"
        tts.save(audio_path)

        text = script

    return render(request, "converter/index.html", {"text": text})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = RegisterForm()

    return render(request, "converter/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")
    else:
        form = AuthenticationForm()

    return render(request, "converter/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/login/")