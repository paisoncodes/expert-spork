"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from decouple import config

from config.health_check import HealthCheck
from utils.views import add_incident_nature, add_incident_type, add_industry, add_superadmin, count_lgas, get_incident_nature, get_incident_type, get_industries, get_states, populate_industries, populate_state, remove_superadmin

schema_view = get_schema_view(
    openapi.Info(
        title="AquilineAlerts APIs",
        default_version="v1",
        description="API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url=config("API_DOCUMENTATION_URL"),
)

def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include("accounts.urls")),
    path('api/v1/profile/', include("accounts_profile.urls")),
    path('api/v1/', include("incident.urls")),
    path('api/v1/', include("subscription.urls")),
    path('api/v1/', include("notifications.urls")),
    path('api/v1/', include("role.urls")),
    path("api/v1/health-check", HealthCheck.as_view(), name="health_check"),
    path('sentry-debug/', trigger_error),
    path('populate-state/', populate_state),
    path('count-lgas/', count_lgas),
    path('populate-industry/', populate_industries),
    path('add-superadmin/', add_superadmin),
    path('add-industry/', add_industry),
    path('add-incident-type/', add_incident_type),
    path('add-incident-nature/', add_incident_nature),
    path('remove-superadmin/', remove_superadmin),
    path('get-states', get_states),
    path('get-industries/', get_industries),
    path('get-incident-type/', get_incident_type),
    path('get-incident-nature/', get_incident_nature)
]

urlpatterns += [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^api/v1/docs/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^api/v1/redoc/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
