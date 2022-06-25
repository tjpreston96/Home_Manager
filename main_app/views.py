import uuid

import boto3
import environ
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import MaintenanceForm, ShoppingForm, TaskForm
from .models import Bill, Note, Photo, Plant, Shopping, Task

env = environ.Env()
environ.Env.read_env()

S3_BASE_URL = env("S3_BASE_URL")
BUCKET = env("BUCKET")

# Create your views here.

# Home
def home(request):
    return render(request, "home.html")


# About
def about(request):
    return render(request, "about.html")


# ===== Accounts =====
def signup(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("about")
        else:
            messages.error(request, "Invalid Sign Up - Please Try Again.", "red-text")

    form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


# ===== Plants =====
@login_required
def plants_index(request):
    plants = Plant.objects.filter(user=request.user)
    return render(request, "plants/index.html", {"plants": plants})


def plants_detail(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    maintenance_form = MaintenanceForm()
    return render(
        request,
        "plants/detail.html",
        {"plant": plant, "maintenance_form": maintenance_form},
    )


class PlantCreate(LoginRequiredMixin, CreateView):
    model = Plant
    fields = [
        "name",
        "description",
        "light",
        "toxicity",
        "environment",
        "watering_frequency",
    ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PlantUpdate(LoginRequiredMixin, UpdateView):
    model = Plant
    fields = [
        "name",
        "description",
        "light",
        "toxicity",
        "environment",
        "watering_frequency",
    ]


class PlantDelete(LoginRequiredMixin, DeleteView):
    model = Plant
    success_url = "/plants/"


# ===== Maintenance (Plants) =====
def add_maintenance(request, plant_id):
    # create a ModelForm instance using the data in request.POST
    form = MaintenanceForm(request.POST)
    # validate the form
    if form.is_valid():
        new_maintenance = form.save(commit=False)
        new_maintenance.plant_id = plant_id
        new_maintenance.save()
    return redirect("plants_detail", plant_id=plant_id)


# ===== S3 Photo (Plants) =====
def add_photo(request, plant_id):
    photo_file = request.FILES.get("photo-file", None)
    if photo_file:
        s3_client = boto3.client("s3")
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind(".") :]
        try:
            s3_client.upload_fileobj(photo_file, BUCKET, key)
            url = f"https://{BUCKET}.s3.amazonaws.com/{key}"
            photo = Photo(url=url, plant_id=plant_id)
            photo.save()
        except:
            print("An error occurred uploading file to S3")
    return redirect("plants_detail", plant_id=plant_id)


# ===== Notes =====
@login_required
def notes_index(request):
    notes = Note.objects.filter(user=request.user)
    return render(request, "notes/index.html", {"notes": notes})


@login_required
def notes_detail(request, note_id):
    note = Note.objects.get(id=note_id)
    if request.user == note.user:
        return render(
            request,
            "notes/detail.html",
            {"note": note},
        )
    else:
        return redirect("notes_index")


class NoteCreate(LoginRequiredMixin, CreateView):
    model = Note
    fields = ["title", "note"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class NoteUpdate(LoginRequiredMixin, UpdateView):
    model = Note
    fields = ["title", "note"]


class NoteDelete(LoginRequiredMixin, DeleteView):
    model = Note
    success_url = "/notes/"


# ===== Tasks =====
@login_required
def tasks_index(request):
    tasks = Task.objects.filter(user=request.user)
    task_form = TaskForm()
    return render(
        request, "tasks/index.html", {"task_list": tasks, "task_form": task_form}
    )


@login_required
def add_task(request):
    form = TaskForm(request.POST)
    form.instance.user = request.user

    if form.is_valid():
        form.save()
        return redirect("tasks_index")


def delete_task(request, task_id):
    obj = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        obj.delete()
        return redirect("tasks_index")


# ===== Bills =====
# @login_required
# def bills_index(request):
#     bills = Bill.objects.filter(user=request.user)
#     return render(request, "bills/index.html", {"bills": bills})


# def bills_detail(request, bill_id):
#     bills = Bill.objects.get(id=bill_id)
#     return render(
#         request,
#         "bills/detail.html",
#         {"bills": bills},
#     )


# class BillCreate(LoginRequiredMixin, CreateView):
#     model = Bill
#     fields = "__all__"

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)


# ===== Shopping =====
@login_required
def shopping_index(request):
    shopping = Shopping.objects.filter(user=request.user)
    shopping_form = ShoppingForm()

    return render(
        request,
        "shopping/index.html",
        {"shopping_list": shopping, "shopping_form": shopping_form},
    )


@login_required
def add_item(request):
    form = ShoppingForm(request.POST)
    form.instance.user = request.user

    if form.is_valid():
        form.save()
        return redirect("shopping_index")


def delete_item(request, shopping_id):
    obj = get_object_or_404(Shopping, id=shopping_id)

    if request.method == "POST":
        obj.delete()
        return redirect("shopping_index")
