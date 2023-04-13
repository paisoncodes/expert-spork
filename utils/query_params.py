from drf_yasg import openapi

YES = "YES"
NO = "NO"

state = openapi.Parameter('state', openapi.IN_QUERY,
                             details="State you want to filter by.",
                             type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))
lga = openapi.Parameter('lga', openapi.IN_QUERY,
                             details="Lga you want to filter by.",
                             type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))
admin_approved = openapi.Parameter('Admin Approved', openapi.IN_QUERY,
                             details=f"{YES}/{NO}",
                             type=openapi.TYPE_STRING)
company_approved = openapi.Parameter('Company Approved', openapi.IN_QUERY,
                             details=f"{YES}/{NO}",
                             type=openapi.TYPE_STRING)
search = openapi.Parameter('search', openapi.IN_QUERY,
                             details="Parameter you want to filter by.",
                             type=openapi.TYPE_STRING)
date = openapi.Parameter('date', openapi.IN_QUERY,
                             details="Date you want to filter by.",
                             type=openapi.TYPE_STRING)
company_name = openapi.Parameter('company_name', openapi.IN_QUERY,
                             details="Company you want to filter by.",
                             type=openapi.TYPE_STRING)
alert_type = openapi.Parameter('alert_type', openapi.IN_QUERY,
                             details="Alert type you want to filter by.",
                             type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))
primary_threat_actor = openapi.Parameter('primary_threat_actor', openapi.IN_QUERY,
                             details="Primary Threat Actor you want to filter by.",
                             type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))
impact = openapi.Parameter('impact', openapi.IN_QUERY,
                             details="Impact you want to filter by.",
                             type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))
threat_level = openapi.Parameter('threat_level', openapi.IN_QUERY,
                             details="Threat Level you want to filter by.",
                             type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))
affected_group = openapi.Parameter('affected_group', openapi.IN_QUERY,
                             details="Affected group you want to filter by.",
                             type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))
incident_nature = openapi.Parameter('incident_nature', openapi.IN_QUERY,
                             details="Incident nature you want to filter by.",
                             type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))
# incident_nature = openapi.Parameter('incident nature', openapi.IN_QUERY,
#                              details="Incident nature you want to filter by.",
#                              type=openapi.TYPE_STRING)
ticket_id = openapi.Parameter('ticket_id', openapi.IN_QUERY,
                             details="ID of ticket you want to retrieve replies for.",
                             type=openapi.TYPE_STRING, required=True)