from typing import Optional

from fastapi import Request
from pydantic import BaseModel, ConfigDict


# Base context shared by all UI templates.
class BasePageContext(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    request: Request
    username: Optional[str] = None
    is_authenticated: bool = False
    role: Optional[str] = None
    flash_success: Optional[str] = None
    flash_error: Optional[str] = None

    # Return context as a dictionary for use in Jinja2.
    def to_dict(self):
        return self.model_dump()
