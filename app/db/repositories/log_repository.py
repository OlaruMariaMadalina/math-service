from sqlalchemy.orm import Session
from app.db.models.log_model import Log


# Return one page of newest logs.
def get_paginated_logs(db: Session, page: int = 1, page_size: int = 20):
    offset = (page - 1) * page_size
    return (
        db.query(Log)
        .order_by(Log.timestamp.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )
