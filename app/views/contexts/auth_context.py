from typing import Optional
from app.views.contexts.base import BasePageContext


# Context for login/register page messages.
class AuthPageContext(BasePageContext):

    login_error: Optional[str] = None
    login_success: Optional[str] = None
    register_error: Optional[str] = None
    register_success: Optional[str] = None
