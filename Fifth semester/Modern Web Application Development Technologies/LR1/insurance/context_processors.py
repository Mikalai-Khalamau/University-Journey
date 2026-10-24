def access_flags(request):
    u = request.user
    staff = (
        u.is_active
        and u.is_authenticated
        and (u.is_superuser or u.groups.filter(name="employee").exists())
    )
    client = u.is_active and u.is_authenticated and u.groups.filter(name="client").exists()
    return {
        "show_crm_tools": staff,
        "is_client_group": client,
    }
