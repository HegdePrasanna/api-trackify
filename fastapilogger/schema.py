from typing import Callable, Union
from pydantic import BaseModel, Field
from datetime import datetime, timedelta

class AuditLog(BaseModel):
    added_on: datetime = datetime.now()
    http_method: Union[str, None] = Field(None)
    api: Union[str, None] = Field(None)
    headers: Union[str, dict] = Field(None)
    payload: Union[dict, None] = Field(None)
    response: Union[dict, str, None] = Field(None)
    client_ip_address: str
    status_code: int = 500
    execution_time: float