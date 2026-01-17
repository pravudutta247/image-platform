import json
from lambdas.upload_image import handler as upload
from lambdas.list_images import handler as list_images

def test_list_images_by_user_is_tenant_isolated():
    # Tenant A upload
    upload({
        "headers": {"x-tenant-id": "tenantA"},
        "body": {
            "user_id": "userX",
            "file": b"imgA",
            "tag": "food"
        }
    }, None)

    # Tenant B upload (same user_id)
    upload({
        "headers": {"x-tenant-id": "tenantB"},
        "body": {
            "user_id": "userX",
            "file": b"imgB",
            "tag": "food"
        }
    }, None)

    resp = list_images({
        "headers": {"x-tenant-id": "tenantA"},
        "queryStringParameters": {
            "user_id": "userX"
        }
    }, None)

    body = json.loads(resp["body"])
    assert resp["statusCode"] == 200
    assert len(body) == 1   # only tenantA data
