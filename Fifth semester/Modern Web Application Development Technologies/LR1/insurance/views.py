"""Re-export FBV CRM handlers (lab: CRUD via function-based views)."""
from django.http import HttpResponse
from django.contrib.auth import get_user_model
import os

def create_admin(request):
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password=os.getenv('ADMIN_PASSWORD', 'admin123')
        )
        return HttpResponse("✅ Superuser created! Username: admin, Password: admin123")
    return HttpResponse("⚠️ Superuser already exists.")


from .crud_views import (  # noqa: F401
    agent_create,
    agent_delete,
    agent_detail,
    agent_list,
    agent_update,
    branch_create,
    branch_delete,
    branch_detail,
    branch_list,
    branch_update,
    client_create,
    client_delete,
    client_detail,
    client_list,
    client_update,
    contract_create,
    contract_delete,
    contract_detail,
    contract_list,
    contract_update,
    insurancetype_create,
    insurancetype_delete,
    insurancetype_detail,
    insurancetype_list,
    insurancetype_update,
    insuredobject_create,
    insuredobject_delete,
    insuredobject_detail,
    insuredobject_list,
    insuredobject_update,
)
