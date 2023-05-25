from django.urls import path, include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.template.exceptions import TemplateDoesNotExist
from django.core.exceptions import ObjectDoesNotExist

urlpatterns = [
    path('', views.index)
]
