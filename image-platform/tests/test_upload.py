from lambdas.upload_image import handler

def test_upload():
    event = {
        "body": {
            "user_id": "u1",
            "file": b"fakeimage",
            "tag": "vacation"
        }
    }
    resp = handler(event, None)
    assert resp["statusCode"] == 200
