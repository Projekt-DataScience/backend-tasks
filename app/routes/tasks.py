from typing import List, Union

from fastapi import APIRouter, Header, HTTPException
from config import dbm
from backend_db_lib.models import User, LPAAudit
from dao.tasks import GetTasksDAO, TaskDAO

from helpers.auth import validate_authorization
router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}, 401: {"description": "Token not valid"}},
)

@router.get("/get-tasks/")
def get_tasks(authorization: Union[str, None] = Header(default=None)) -> GetTasksDAO:
    payload = validate_authorization(authorization)
    user_id = int(payload['user_id'])

    with dbm.create_session() as session:
        user = session.query(User).get(user_id)
        if user is None:
            raise HTTPException(
                status_code=401, detail="Token not valid")

        # combine multiple tasks later if more than lpa tasks are needed
        lpa_tasks = get_tasks_lpa(session, user)

        return GetTasksDAO(
            tasks=lpa_tasks,
        )


def get_tasks_lpa(session, user) -> List[TaskDAO]:
    layer_id = user.layer_id
    group_id = user.group_id
    if (layer_id is not None) and (group_id is not None):
        audits = session.query(LPAAudit).filter(
            (
                    (LPAAudit.assigned_group_id == group_id) |
                    (LPAAudit.assigned_layer_id == layer_id) |
                    (LPAAudit.audited_user_id == user.id)
            ) &
            (LPAAudit.complete_datetime.is_(None))
        )

        tasks = []
        for audit in audits:
            assignee = f"Gruppe '{audit.assigned_group.group_name}'" if audit.assigned_group is not None \
                else f"Ebene '{audit.assigned_layer.layer_name}'"
            recurrence = ('Spontaner' if audit.recurrent_audit else 'Geplanter')

            title = f"{recurrence} Audit für {assignee}"

            task = TaskDAO(
                icon='lpa',
                app_name='lpa',
                title=title,
                action='audit',
                parameter=f'{audit.id}',
                date=str(audit.due_date),
                layer=audit.assigned_layer.layer_number,
                group=audit.assigned_group.group_name,
            )
            tasks.append(task)
        return tasks
    return []
