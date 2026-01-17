def get_tenant_id(event):
    tenant_id = event.get("headers", {}).get("x-tenant-id")
    if not tenant_id:
        raise ValueError("Missing x-tenant-id header")
    return tenant_id
