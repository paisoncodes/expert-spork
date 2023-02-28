from django.urls import path

from role.views import RolePermissionsView, RoleRetrieveUpdateView, RoleView


urlpatterns = [
    path("roles/", RoleView.as_view(),),
    path("roles/details/<str:role_id>/", RoleRetrieveUpdateView.as_view(),),
    path("roles/permissions/", RolePermissionsView.as_view(),),
]