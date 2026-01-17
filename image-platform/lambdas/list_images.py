from botocore.exceptions import ClientError
from common.db import table
from common.auth import get_tenant_id
from common.response import success, error

def handler(event, context):
    try:
        tenant_id = get_tenant_id(event)
        params = event.get("queryStringParameters") or {}

        user_id = params.get("user_id")
        tag = params.get("tag")

        if user_id:
            resp = table.query(
                IndexName="user-index",
                KeyConditionExpression="gsi_user_pk = :pk",
                ExpressionAttributeValues={
                    ":pk": f"{tenant_id}#{user_id}"
                }
            )
        elif tag:
            resp = table.query(
                IndexName="tag-index",
                KeyConditionExpression="gsi_tag_pk = :pk",
                ExpressionAttributeValues={
                    ":pk": f"{tenant_id}#{tag}"
                }
            )
        else:
            return error("At least one filter is required")

        return success(resp.get("Items", []))

    except ValueError as e:
        return error(str(e), 401)

    except ClientError:
        return error("AWS error", 500)

    except Exception:
        return error("Internal server error", 500)
