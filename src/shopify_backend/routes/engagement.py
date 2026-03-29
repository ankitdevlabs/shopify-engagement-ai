from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from shopify_backend.dependencies.common import get_engagement_service
from shopify_backend.models.entities import EngagementRequest
from shopify_backend.service.engagement_service import EngagementService

router = APIRouter(tags=["engagement"])


@router.post("/analyze")
async def track_event(
    payload: EngagementRequest,
    service: EngagementService = Depends(get_engagement_service),
):
    return await service.analyze_session(payload)


@router.options("/analyze")
async def options_analyze():
    """Handle CORS preflight"""
    return JSONResponse(
        content={"message": "OK"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        },
    )
