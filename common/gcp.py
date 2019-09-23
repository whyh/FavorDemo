from os import getenv

PROJECT_ID = getenv("GCP_PROJECT_ID")
GAE_ZONE = getenv("GAE_ZONE")
FIN_IP = getenv("GCP_FIN_IP")

GCP_WITHDRAW_QUEUE = getenv("GCP_WITHDRAW_QUEUE")
GCP_WITHDRAW_QUEUE_ZONE = getenv("GCP_WITHDRAW_QUEUE_ZONE")
WITHDRAW_HANDLER_ROUTE = "withdraw"
WITHDRAW_HANDLER_URL = f"http://{getenv('GCP_FIN_IP')}:8080/{WITHDRAW_HANDLER_ROUTE}"
