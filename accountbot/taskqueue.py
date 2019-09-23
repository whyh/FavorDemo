from datetime import datetime
from typing import Optional

from google.cloud.tasks_v2beta3 import CloudTasksClient
from google.protobuf.timestamp_pb2 import Timestamp

from common import sed, gcp

client = CloudTasksClient()
stamp = Timestamp()

WITHDRAW_PATH = client.queue_path(gcp.PROJECT_ID, gcp.GCP_WITHDRAW_QUEUE_ZONE, gcp.GCP_WITHDRAW_QUEUE)
WITHDRAW_TEMPLATE = {"http_request": {"http_method": "POST", "url": gcp.WITHDRAW_HANDLER_URL}}


def create_withdraw_task(user: int, card: str, amount: str, wait_until: Optional[datetime] = None) -> None:
    task = WITHDRAW_TEMPLATE.copy()
    task["http_request"]["body"] = sed.encode(**{sed.kv.USER: user, sed.kv.CARD: card, sed.kv.AMOUNT: amount}).encode()
    task["schedule_time"] = stamp.FromDatetime(datetime.utcnow() if wait_until is None else wait_until)
    client.create_task(WITHDRAW_PATH, task)
