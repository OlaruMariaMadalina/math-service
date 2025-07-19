import redis
import json
from datetime import datetime, timezone

from app.db.models.log_model import Log
from app.db.models.user_model import User
from app.db.database import SessionLocal, init_db
from app.utils.config import settings

def start_log_worker():
    print(">>>>>>>> STARTED WORKER SCRIPT <<<<<<<<")

    # Connect to Redis
    r = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True
    )
    pubsub = r.pubsub()
    pubsub.subscribe("logs")

    print("[WORKER] Connected. Waiting for messages...")

    # Initialize database tables
    init_db()
    print("[LOG WORKER] Listening on 'logs' channel...")

    # Infinite loop: listen for new log messages
    for message in pubsub.listen():
        if message["type"] != "message":
            continue

        try:
            data = json.loads(message["data"])

            log = Log(
                event=data.get("event"),
                level=data.get("level"),
                timestamp=datetime.now(timezone.utc),
                user=data.get("user"),
                operation=data.get("operation"),
                input=json.dumps(data.get("input", {})),
                result=data.get("result", "no result")
            )

            db = SessionLocal()
            db.add(log)
            db.commit()

            op = log.operation
            user = log.user

            db.close()

            print(f"[LOG SAVED] {op} by {user}")

        except Exception as e:
            print(f"[ERROR] Failed to save log: {e}")

start_log_worker()