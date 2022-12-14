from typing import List

from pydantic import BaseModel

class TaskDAO(BaseModel):
    icon: str
    app_name : str
    title : str
    date : str
    parameter : str
    id : int

class GetTasksDAO(BaseModel):
    result : int
    tasks : List[TaskDAO]

