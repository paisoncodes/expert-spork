from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsVerified
from notifications.models import Notification
from notifications.serializers import NotificationSerialzier
from utils.utils import api_response




class NotificationView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVerified]
    serializer_class = NotificationSerialzier

    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(user=user)
        serializer = self.serializer_class(notifications, many=True)

        return api_response("Notifications fetched", serializer.data, True, 200)
