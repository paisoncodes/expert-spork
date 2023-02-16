from django.urls import path

from notifications.views import NotificationView 




urlpatterns = [
    path("notifications/", NotificationView.as_view()),
]