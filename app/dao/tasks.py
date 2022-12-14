from typing import List

from pydantic import BaseModel

class TaskDAO(BaseModel):
    icon: str
    app_name : str
    title : str
    parameter : str
    date : str
    layer : int
    group : str

class GetTasksDAO(BaseModel):
    tasks : List[TaskDAO]

