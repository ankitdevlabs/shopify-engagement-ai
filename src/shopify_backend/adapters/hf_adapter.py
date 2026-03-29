import json

import httpx
from loguru import logger


class HFAdapter:
    logger = logger

    def __init__(self, settings):
        self.settings = settings

    async def prepare_header(self):
        return {
            "Authorization": f"Bearer {self.settings.hf_api_key}",
            "Content-Type": "application/json",
        }

    async def make_api_request(
        self,
        method: str,
        url: str,
        headers: dict[str, any] | None = None,
        params: dict[str, any] | None = None,
        data: dict[str, any] | None = None,
        json: dict[str, any] | None = None,
        timeout: float = 20.0,
    ) -> any:
        """
        Asynchronous HTTP request function.

        Args:
            method (str): HTTP method (GET, POST, PUT, etc.).
            url (str): Full URL to make the request to.
            headers (Optional[Dict[str, any]]): Headers to include.
            params (Optional[Dict[str, any]]): URL query parameters.
            data (Optional[Dict[str, any]]): JSON body data.
            timeout (float): Timeout for the request in seconds.

        Returns:
            Optional[any]: Parsed JSON response or an error dict.
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    data=data,
                    json=json,
                    timeout=timeout,
                )

                response.raise_for_status()

                if response.status_code == 204:
                    return {"status": "success", "message": "No content"}

                try:
                    return response.json()
                except ValueError:
                    self.logger.error("Failed to parse JSON from response")
                    return {"error": "Invalid JSON response"}

            except httpx.HTTPStatusError as e:
                self.logger.error(
                    f"HTTP error {e.response.status_code}: {e.response.url} - {e.response.text}"
                )
                return {"error": f"HTTP error {e.response.status_code}"}

            except httpx.TimeoutException:
                self.logger.error("Request timed out")
                return {"error": "Request timed out"}

            except httpx.NetworkError:
                self.logger.error("Network error occurred")
                return {"error": "Network error occurred"}

            except httpx.RequestError as e:
                self.logger.error(f"Request error: {str(e)}")
                return {"error": f"Request error: {str(e)}"}

            except Exception as e:
                self.logger.error(f"Unexpected error: {str(e)}")
                return {"error": f"Unexpected error: {str(e)}"}

    async def get_response(self, prompt: str) -> str:
        headers = await self.prepare_header()

        payload = {
            "model": self.settings.hf_model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a Shopify store engagement assistant. "
                        "Analyze user session data and return ONLY valid JSON like "
                        '{"show_message": true/false, "message": "under 100 chars", '
                        '"priority": "high|medium|low", "reason": "brief explanation"}'
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        }

        # response = await self.make_api_request(
        #     method="POST",
        #     url=f"{self.settings.hf_base_uri}/chat/completions",
        #     headers=headers,
        #     json=payload,
        #     timeout=50.0,
        # )

        # if response.get("error"):
        #     self.logger.error(f"Error from HF API: {response['error']}")
        #     return {
        #         "show_message": False,
        #         "message": "",
        #         "priority": "low",
        #         "reason": f"HF API error: {response.get('error')}",
        #     }

        # content_str = (
        #     (response.get("choices", [{}]) or [{}])[0].get("message", {}) or {}
        # ).get("content", "") or ""

        # if not content_str:
        #     self.logger.warning("HF API returned empty content")
        #     return {
        #         "show_message": False,
        #         "message": "",
        #         "priority": "low",
        #         "reason": "HF API returned empty content",
        #     }

        # try:
        #     data = json.loads(content_str)
        #     return {
        #         "show_message": data.get("show_message", False),
        #         "message": data.get("message", ""),
        #         "priority": data.get("priority", "low"),
        #         "reason": data.get("reason", ""),
        #     }
        # except json.JSONDecodeError:
        #     self.logger.error(f"Failed to parse HF response as JSON: {content_str}")
        #     return {
        #         "show_message": False,
        #         "message": "",
        #         "priority": "low",
        #         "reason": "Invalid JSON from HF API",
        #     }
