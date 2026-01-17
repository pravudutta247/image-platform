import json
from lambdas.upload_image import handler as upload
from lambdas.get_image import handler as get_image

def test_get_image_cross_tenant_blocked():
    upload_resp = upload({
        "headers": {"x-tenant-id": "tenantA"},
        "body": {
            "user_id": "user1",
            "file": b"img",
            "tag": "pets"
        }
    }, None)

    image_id = json.loads(upload_resp["body"])["image_id"]

    # Try to access from another tenant
    resp = get_image({
        "headers": {"x-tenant-id": "tenantB"},
        "pathParameters": {
            "image_id": image_id
        }
    }, None)

    assert resp["statusCode"] == 404
