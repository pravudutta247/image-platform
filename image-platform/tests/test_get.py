from lambdas.upload_image import handler as upload
from lambdas.get_image import handler as get_image

def test_get_image():
    upload_resp = upload({
        "body": {
            "user_id": "u99",
            "file": b"img99",
            "tag": "pets"
        }
    }, None)

    image_id = upload_resp["body"]["image_id"]

    resp = get_image({
        "pathParameters": {
            "image_id": image_id
        }
    }, None)

    assert resp["statusCode"] == 200
    assert "url" in resp["body"]
