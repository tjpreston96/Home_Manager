from django.urls import URLPattern, path
from django.conf import settings

from . import views

urlpatterns = [
    # ===== Main =====
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    # ===== Accounts =====
    path("accounts/signup/", views.signup, name="signup"),
    # ===== Tasks =====
    path("tasks/", views.tasks_index, name="tasks_index"),
    # path("tasks/<int:task_id>/", views.tasks_detail),
    # path("tasks/create/", views.TaskCreate.as_view(), name="tasks_create"),
    # ===== Plants =====
    path("plants/", views.plants_index, name="plants_index"),
    path("plants/<int:plant_id>/", views.plants_detail, name="plants_detail"),
    path("plants/create/", views.PlantCreate.as_view(), name="plants_create"),
    path("plants/<int:pk>/update/", views.PlantUpdate.as_view(), name="plants_update"),
    path("plants/<int:pk>/delete/", views.PlantDelete.as_view(), name="plants_delete"),
    path(
        "plants/<int:plant_id>/add_maintenance/",
        views.add_maintenance,
        name="add_maintenance",
    ),
    path("plants/<int:plant_id>/add_photo/", views.add_photo, name="add_photo"),
    # ===== Bills =====
    # path("bills/", views.bills_index, name="bills_index"),
    # path("bills/<int:bill_id>/", views.bills_detail, name="bills_detail"),
    # path("bills/create/", views.BillCreate.as_view(), name="bills_create"),
    # ===== Shopping =====
    path("shopping/", views.shopping_index, name="shopping_index"),
    path('shopping/create/', views.add_item, name='add_item'),
    path('shopping/<int:shopping_id>/delete/', views.delete_item, name='delete_item'),
    # path("shopping/create/", views.ShoppingCreate.as_view(), name="shopping_create"),
    # ===== Notes =====
    path("notes/", views.notes_index, name="notes_index"),
    path("notes/<int:note_id>/", views.notes_detail, name="notes_detail"),
    path("notes/create/", views.NoteCreate.as_view(), name="notes_create"),
    # path("notes/create/add/", views.add_note, name="add_note"),
    path("notes/<int:pk>/update/", views.NoteUpdate.as_view(), name="notes_update"),
    path("notes/<int:pk>/delete/", views.NoteDelete.as_view(), name="notes_delete"),
    # ===== Accounts =====
    path("accounts/signup/", views.signup, name="signup"),
]
