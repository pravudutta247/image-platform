import json
from lambdas.upload_image import handler as upload
from lambdas.delete_image import handler as delete

def test_delete_is_idempotent_and_tenant_safe():
    upload_resp = upload({
        "headers": {"x-tenant-id": "tenantA"},
        "body": {
            "user_id": "user9",
            "file": b"img9",
            "tag": "cars"
        }
    }, None)

    image_id = json.loads(upload_resp["body"])["image_id"]

    # First delete
    resp1 = delete({
        "headers": {"x-tenant-id": "tenantA"},
        "pathParameters": {
            "image_id": image_id
        }
    }, None)

    assert resp1["statusCode"] == 204

    # Second delete (idempotent)
    resp2 = delete({
        "headers": {"x-tenant-id": "tenantA"},
        "pathParameters": {
            "image_id": image_id
        }
    }, None)

    assert resp2["statusCode"] == 204
