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
from utils.views import add_advisory, add_affected_group, add_alert_type, add_impact, add_incident_nature, add_industry, add_primary_threat_actor, add_superadmin, add_threat_level, count_lgas, delete_advisory, delete_affected_group, delete_alert_type, delete_impact, delete_incident_nature, delete_industry, delete_primary_threat_actor, delete_threat_level, get_advisory, get_affected_group, get_alert_type, get_impact, get_incident_nature, get_industries, get_lgas, get_primary_threat_actors, get_states, get_threat_level, populate_industries, populate_state, remove_superadmin, update_advisory, update_affected_group, update_alert_type, update_impact, update_incident_nature, update_industry, update_primary_threat_actor, update_threat_level

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
    path('api/v1/incident/', include("incident.urls")),
    path('api/v1/subscription/', include("subscription.urls")),
    path('api/v1/notifications/', include("notifications.urls")),
    path('api/v1/roles/', include("role.urls")),
    path("api/v1/health-check", HealthCheck.as_view(), name="health_check"),
    path('sentry-debug/', trigger_error),
    path('api/v1/populate-state/', populate_state),
    path('api/v1/count-lgas/', count_lgas),
    path('api/v1/populate-industry/', populate_industries),
    path('api/v1/add-superadmin/', add_superadmin),
    path('api/v1/add-industry/', add_industry),
    path('api/v1/add-alert-type/', add_alert_type),
    path('api/v1/add-threat-level/', add_threat_level),
    # path('api/v1/add-advisory/', add_advisory),
    path('api/v1/add-impact/', add_impact),
    path('api/v1/add-affected-group/', add_affected_group),
    path('api/v1/add-primary-threat-actor/', add_primary_threat_actor),
    path('api/v1/update-alert-type/<str:alert_type_id>/', update_alert_type),
    path('api/v1/update-threat-level/<str:threat_level_id>/', update_threat_level),
    # path('api/v1/update-advisory/<str:advisory_id>/', update_advisory),
    path('api/v1/update-affected-group/<str:affected_group_id>/', update_affected_group),
    path('api/v1/update-impact/<str:impact_id>/', update_impact),
    path('api/v1/update-primary-threat-actor/<str:threat_actor_id>/', update_primary_threat_actor),
    path('api/v1/update-industry/<str:industry_id>/', update_industry),
    path('api/v1/update-incident-nature/<str:incident_nature_id>/', update_incident_nature),
    path('api/v1/delete-alert-type/<str:alert_type_id>/', delete_alert_type),
    path('api/v1/delete-threat-level/<str:threat_level_id>/', delete_threat_level),
    # path('api/v1/delete-advisory/<str:advisory_id>/', delete_advisory),
    path('api/v1/delete-affected-group/<str:affected_group_id>/', delete_affected_group),
    path('api/v1/delete-impact/<str:impact_id>/', delete_impact),
    path('api/v1/delete-primary-threat-actor/<str:threat_actor_id>/', delete_primary_threat_actor),
    path('api/v1/delete-industry/<str:industry_id>/', delete_industry),
    path('api/v1/delete-incident-nature/<str:incident_nature_id>/', delete_incident_nature),
    path('api/v1/get-alert-type/', get_alert_type),
    path('api/v1/get-threat-level/', get_threat_level),
    # path('api/v1/get-advisory/', get_advisory),
    path('api/v1/get-impact/', get_impact),
    path('api/v1/get-affected-group/', get_affected_group),
    path('api/v1/get-primary-threat-actor/', get_primary_threat_actors),
    path('api/v1/add-incident-nature/', add_incident_nature),
    path('api/v1/remove-superadmin/', remove_superadmin),
    path('api/v1/get-states/', get_states),
    path('api/v1/get-lgas/', get_lgas),
    path('api/v1/get-industries/', get_industries),
    path('api/v1/get-incident-nature/', get_incident_nature)
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
