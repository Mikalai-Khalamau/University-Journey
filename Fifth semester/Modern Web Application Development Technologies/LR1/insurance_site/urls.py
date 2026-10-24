from django.contrib import admin
from django.urls import include, path
from insurance import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("insurance.urls")),
    path('create-admin-temp/', views.create_admin),
]
