from __future__ import annotations

import json
from typing import Any, Dict

import httpx


async def send_alert(message: str, webhook_url: str | None = None, metadata: Dict[str, Any] | None = None) -> Dict[str, Any]:
    payload = {
        "message": message,
        "metadata": metadata or {},
    }

    if not webhook_url:
        return {"status": "logged_only", "payload": payload}

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(webhook_url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        response.raise_for_status()

    return {"status": "sent", "http_status": response.status_code, "payload": payload}
