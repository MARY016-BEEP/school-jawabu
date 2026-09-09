from database import SessionLocal
from models import AuditLog


def log_action(
    username,
    user_role,
    action,
    table_name,
    record_id,
    description,
    old_value="",
    new_value=""
):

    db = SessionLocal()

    log = AuditLog(

        username=username,

        user_role=user_role,

        action=action,

        table_name=table_name,

        record_id=str(record_id),

        description=description,

        old_value=str(old_value),

        new_value=str(new_value)

    )

    db.add(log)

    db.commit()

    db.close()
