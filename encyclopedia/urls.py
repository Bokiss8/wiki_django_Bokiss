from django.conf.urls import url
from django.urls import path

from . import views
app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wpages, name="wpages"),
    path("wiki/", views.poisk, name="poisk"),
    path("createpage", views.createpage, name="createpage"),
    path("correctpage/<str:title>", views.correctpage, name="correctpage"),
    path("correctpagesave",views.correctpagesave, name="correctpagesave"),
    path("randompage", views.randompage, name="randompage")
]
