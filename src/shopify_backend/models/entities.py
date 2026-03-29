from pydantic import BaseModel


class EngagementRequest(BaseModel):
    session_id: str
    event_type: str
    current_page: str
    cart_items: int
    time_on_site: int

    element: str | None = None
    text: str | None = None
