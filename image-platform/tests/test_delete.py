from lambdas.upload_image import handler as upload
from lambdas.delete_image import handler as delete

def test_delete_image():
    upload_resp = upload({
        "body": {
            "user_id": "u5",
            "file": b"img5",
            "tag": "cars"
        }
    }, None)

    image_id = upload_resp["body"]["image_id"]

    resp = delete({
        "pathParameters": {
            "image_id": image_id
        }
    }, None)

    assert resp["statusCode"] == 204
