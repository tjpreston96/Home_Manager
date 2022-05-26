from django.urls import URLPattern, path
from . import views

urlpatterns = [
    # ===== Main =====
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    # ===== Chores =====
    path("chores/", views.chores_index, name="chores_index"),
    # ===== Plants =====
    # ===== Bills =====
    # ===== Shopping =====
    # ===== Notes =====
]
