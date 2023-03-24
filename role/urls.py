from django.urls import path

from role.views import RolePermissionRetrieveUpdateDeleteView, RolePermissionsView, RoleRetrieveUpdateDeleteView, RoleView, UserRoleAndPermissionsView


urlpatterns = [
    path("roles/", RoleView.as_view(),),
    path("roles/details/<str:role_id>/", RoleRetrieveUpdateDeleteView.as_view(),),
    path("roles/permissions/", RolePermissionsView.as_view(),),
    path("roles/permissions/<str:permission_id>/edit/", RolePermissionRetrieveUpdateDeleteView.as_view(),),
    path("roles/<str:user_id>/role/", UserRoleAndPermissionsView.as_view(),),
]