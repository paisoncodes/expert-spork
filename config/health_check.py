from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import serializers


class HealthCheckSerializer(serializers.Serializer):
    lol = serializers.CharField()


class HealthCheck(GenericAPIView):
    serializer_class = HealthCheckSerializer

    def get(self, request):
        return Response({"message": "healthy"})
