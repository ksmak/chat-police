from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from chats.views import (
    ChatViewSet,
    FileUploadView,
)
from auths.views import (
    CustomAuthToken,
    UsersViewSet,
)

router = routers.DefaultRouter()
router.register(r"chats", ChatViewSet, basename="chats")
router.register(r"users", UsersViewSet, basename="users")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", CustomAuthToken.as_view()),
    path("api/", include(router.urls)),
    path("api/uploadfile/", FileUploadView.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
