from shopify_backend.adapters.hf_adapter import HFAdapter
from shopify_backend.models.entities import EngagementRequest


class EngagementService:

    def __init__(self, adapter: HFAdapter):
        self.adapter = adapter

    async def analyze_session(self, payload: EngagementRequest):
        prompt = await self._build_prompt(payload)

        result = await self.adapter.get_response(prompt)

        return result

    async def _build_prompt(self, payload: EngagementRequest) -> str:
        """Build concise LLM prompt from engagement request"""

        # Build brief event context
        events = f"[{payload.event_type}]"
        if payload.element:
            events += f" on {payload.element}"
        if payload.text:
            events += f" with text: {payload.text[:50]}"

        return f"""
            You are a Shopify engagement assistant. Decide if a personalized message should be shown.

            Session:
            - Page: {payload.current_page}
            - Cart Items: {payload.cart_items}
            - Time on Site: {payload.time_on_site}s
            - Event: {events}

            Rules:
            1. Show message if time_on_site >120s and cart_items>0
            2. Show message if hesitation (multiple views/cart changes)
            3. Never repeat message within 5min
            4. Message <100 chars, relevant to page and event

            Return ONLY JSON:
            {{
            "show_message": boolean,
            "message": "short message",
            "priority": "high|medium|low",
            "reason": "brief explanation"
            }}
        """
