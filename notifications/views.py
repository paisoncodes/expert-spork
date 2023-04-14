from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsVerifiedAndActive
from notifications.models import Notification
from notifications.serializers import NotificationSerialzier
from utils.utils import api_response
from drf_yasg.utils import swagger_auto_schema




class NotificationView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedAndActive]
    serializer_class = NotificationSerialzier

    @swagger_auto_schema(operation_summary="View user notifications.")
    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(user=user)
        serializer = self.serializer_class(notifications, many=True)

        return api_response("Notifications fetched", serializer.data, True, 200)
