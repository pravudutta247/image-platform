import json
from lambdas.upload_image import handler

def test_upload_image_success():
    event = {
        "headers": {"x-tenant-id": "tenantA"},
        "body": {
            "user_id": "user1",
            "file": b"image-bytes",
            "tag": "travel"
        }
    }

    resp = handler(event, None)

    body = json.loads(resp["body"])
    assert resp["statusCode"] == 201
    assert "image_id" in body


def test_upload_missing_tenant():
    event = {
        "body": {
            "user_id": "user1",
            "file": b"image"
        }
    }

    resp = handler(event, None)
    assert resp["statusCode"] == 401
