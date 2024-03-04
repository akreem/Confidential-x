from django.urls import path
from . import views

urlpatterns = [
    path("personnes/<param>", views.personnes, name="personnes"),
    path("personnes/", views.personnesAPI, name="personnesAPI"),
    path("enqext/<cin>", views.enqext, name="enqext")

]