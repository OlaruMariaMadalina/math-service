import json
import logging
from datetime import datetime, timezone

import redis

from app.db.models.log_model import Log
from app.db.database import SessionLocal, init_db
from app.utils.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


# Start the log worker that listens to Redis and saves logs to the DB.
def start_log_worker():

    logger.info(">>>>>>>> STARTING LOG WORKER <<<<<<<<<<")

    # Connect to Redis
    try:
        r = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True,
        )
        pubsub = r.pubsub()
        pubsub.subscribe("logs")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        return

    logger.info("[WORKER] Connected. Waiting for messages...")

    # Initialize DB tables if not created
    init_db()
    logger.info(
        "[WORKER] Database initialized. Listening on 'logs' channel..."
    )

    # Loop to process messages from Redis
    for message in pubsub.listen():
        if message.get("type") != "message":
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
                result=data.get("result", "no result"),
            )

            # Save log to DB using context manager
            with SessionLocal() as db:
                db.add(log)
                db.commit()

                # Access values before session closes
                op = log.operation
                user = log.user

            logger.info(f"[LOG SAVED] {op} by {user}")

        except Exception as e:
            logger.exception(f"[ERROR] Failed to save log: {e}")


# Only run if executed directly (not on import)
if __name__ == "__main__":
    start_log_worker()
