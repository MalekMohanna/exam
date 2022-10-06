from django.urls import path 
from .import views

urlpatterns = [
    path("", views.index),
    path("create_user", views.create_user),
    path("dashboard", views.success),
    path("logout", views.logout),
    path("login",views.proc_login),
    path('plant/',views.plant),
    path('addplant',views.addplant),
    path('account/',views.account),
    path('edit/<int:id>/',views.edit),
    path('edit_tree',views.edit_tree),
    path('show/<int:id>/',views.show),
    path('visit/<int:id>',views.visit),
    path('delete/<int:id>',views.delete),
]