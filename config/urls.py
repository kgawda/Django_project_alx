from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework import routers

from devboard.api_views import CommentViewSet, TaskViewSet

router = routers.DefaultRouter()
router.register("comments", CommentViewSet, basename="comment")
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("devboard.urls", namespace="devboard")),
    path("api/v1/", include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(), name="docs"),
    path("api/docs/redoc", SpectacularRedocView.as_view(), name="redoc"),
]
