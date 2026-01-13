from lambdas.upload_image import handler as upload
from lambdas.list_images import handler as list_images

def test_list_by_user():
    upload({
        "body": {
            "user_id": "user123",
            "file": b"img1",
            "tag": "nature"
        }
    }, None)

    resp = list_images({
        "queryStringParameters": {
            "user_id": "user123"
        }
    }, None)

    assert resp["statusCode"] == 200
    assert len(resp["body"]) >= 1


def test_list_by_tag():
    resp = list_images({
        "queryStringParameters": {
            "tag": "nature"
        }
    }, None)

    assert resp["statusCode"] == 200
    assert len(resp["body"]) >= 1
