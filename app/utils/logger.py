import redis
import json
from typing import Dict, Any

from app.utils.config import settings


# Initialize Redis client connection
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)


# Publish a structured log message to a Redis channel
def publish_log(channel: str, message: dict):
    print("publish log")
    try:
        if not isinstance(message, dict):
            raise ValueError(
                "Message must be a dictionary for JSON serialization."
                )
        if not isinstance(channel, str) or not channel:
            raise ValueError("Channel must be a non-empty string.")
        print("[PUBLISH_LOG]", json.dumps(message, default=str))
        r.publish(channel, json.dumps(message))
    except Exception:
        try:
            with open("log_fallback.log", "a") as f:
                f.write(f"[{channel}] {str(message)}\n")
        except Exception as file_error:
            print(f"[FATAL] Even fallback file logging failed: {file_error}")


# Build a dictionary representing a log message
def build_log_message(
    operation: str,
    input_data: Dict[str, Any],
    result: Any,
    user: str,
    level: str = "INFO",
    event: str = "operation_completed"
) -> Dict[str, Any]:
    return {
        "event": event,
        "level": level,
        "user": user,
        "operation": operation,
        "input": input_data,
        "result": result
    }
