from django.urls import path
from rest_framework.routers import SimpleRouter

from lms.apps import LmsConfig
from lms.views import (CourseViewSet, LessonCreateApiView,
                       LessonDestroyApiView, LessonListApiView,
                       LessonRetrieveApiView, LessonUpdateApiView, SubscriptionView)

app_name = LmsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet),


urlpatterns = [
    path("lessons/", LessonListApiView.as_view(), name="lessons-list"),
    path("lessons/<int:pk>/", LessonRetrieveApiView.as_view(), name="lessons-detail"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lessons-create"),
    path("lessons/<int:pk>/delete/", LessonDestroyApiView.as_view(), name="lessons-delete"),
    path(
        "lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lessons-update",
    ),
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
]

urlpatterns += router.urls
