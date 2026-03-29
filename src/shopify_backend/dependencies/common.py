from fastapi import Depends, Request

from shopify_backend.adapters.hf_adapter import HFAdapter
from shopify_backend.service.engagement_service import EngagementService


def get_settings(request: Request):
    return request.app.state.settings


def get_engagement_service(settings=Depends(get_settings)):
    adapter = HFAdapter(settings)
    return EngagementService(adapter)
