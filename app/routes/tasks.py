from typing import List, Union

from fastapi import APIRouter, HTTPException, Header
from config import dbm
from backend_db_lib.models import User, LPAAudit

from auth_handler import TokenData
from dao.tasks import GetTasksDAO, TaskDAO
from pydantic import BaseModel

from app.helpers import validate_authorization

router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}, 401: {"description": "Token not valid"}},
)


@router.post("/get-tasks/")
def get_tasks(authorization: Union[str, None] = Header(default=None)) -> GetTasksDAO:
    payload = validate_authorization(authorization)
    user_id = payload['user_id']

    with dbm.create_session() as session:
        user = session.query(User).get(user_id)
        if user is None:
            return GetTasksDAO(result=0, tasks=[])

        # combine multiple tasks later if more than lpa tasks are needed
        lpa_tasks = get_tasks_lpa(session, user)

        return GetTasksDAO(
            result=1,
            tasks=lpa_tasks,
        )


def get_tasks_lpa(session, user) -> List[TaskDAO]:
    layer_id = user.layer_id
    group_id = user.group_id

    if (layer_id is not None) and (group_id is not None):
        audits = session.query(LPAAudit).filter(
            (LPAAudit.assigned_group_id == group_id) |
            (LPAAudit.assigned_layer_id == layer_id) & (LPAAudit.complete_datetime is None)
        )

        tasks = []
        for audit in audits:
            assignee = ('Gruppe ' + audit.group.name) if audit.group is not None else ('Ebene ' + audit.layer.name)
            recurrence = ('Spontaner' if audit.recurrent_audit else 'Geplanter')

            title = f'{assignee} Audit in {recurrence}'

            task = TaskDAO(
                icon='lpa',
                app_name='lpa',
                title=title,
                action='audit',
                parameter=f'{audit.id}'
            )
            tasks.append(task)
        return tasks
    return []
