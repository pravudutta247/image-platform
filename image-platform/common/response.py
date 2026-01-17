import json

def success(body, status_code=200):
    return {
        "statusCode": status_code,
        "body": json.dumps(body),
        "headers": {
            "Content-Type": "application/json"
        }
    }

def error(message, status_code=400):
    return {
        "statusCode": status_code,
        "body": json.dumps({
            "error": message
        }),
        "headers": {
            "Content-Type": "application/json"
        }
    }
