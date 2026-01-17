import uuid
import time
from botocore.exceptions import ClientError

from common.db import table
from common.s3 import s3, BUCKET
from common.auth import get_tenant_id
from common.response import success, error

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

def handler(event, context):
    try:
        tenant_id = get_tenant_id(event)
        body = event.get("body") or {}

        user_id = body.get("user_id")
        file_bytes = body.get("file")
        tag = body.get("tag", "general")

        if not user_id or not file_bytes:
            return error("user_id and file are required")

        if len(file_bytes) > MAX_FILE_SIZE:
            return error("File too large", 413)

        image_id = str(uuid.uuid4())
        created_at = str(int(time.time()))

        s3_key = f"{tenant_id}/{user_id}/{image_id}.jpg"

        s3.put_object(
            Bucket=BUCKET,
            Key=s3_key,
            Body=file_bytes
        )

        table.put_item(Item={
            "tenant_id": tenant_id,
            "image_id": image_id,
            "created_at": created_at,
            "user_id": user_id,
            "tag": tag,
            "gsi_user_pk": f"{tenant_id}#{user_id}",
            "gsi_tag_pk": f"{tenant_id}#{tag}",
            "s3_bucket": BUCKET,
            "s3_key": s3_key
        })

        return success({"image_id": image_id}, 201)

    except ValueError as e:
        return error(str(e), 401)

    except ClientError:
        return error("AWS error", 500)

    except Exception:
        return error("Internal server error", 500)
