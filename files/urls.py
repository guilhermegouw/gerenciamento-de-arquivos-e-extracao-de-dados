from django.urls import path

from .views import (
    FileListView,
    FileUploadView,
    UserListDescView,
    UserListView,
    UserMaxSizeView,
    UserMinSizeView,
    UserRangeMessagesView,
)

urlpatterns = [
    path("upload/", FileUploadView.as_view(), name="file_upload"),
    path("files/", FileListView.as_view(), name="file_list"),
    path(
        "files/user_max_size/<str:file_name>/",
        UserMaxSizeView.as_view(),
        name="user_max_size",
    ),
    path(
        "files/user_min_size/<str:file_name>/",
        UserMinSizeView.as_view(),
        name="user_min_size",
    ),
    path(
        "files/users/<str:file_name>/",
        UserListView.as_view(),
        name="user_list",
    ),
    path(
        "files/users_desc/<str:file_name>/",
        UserListDescView.as_view(),
        name="user_list_desc",
    ),
    path(
        "files/users_range_messages/<str:file_name>/<int:min_msgs>/"
        "<int:max_msgs>/",
        UserRangeMessagesView.as_view(),
        name="user_range_messages",
    ),
]
