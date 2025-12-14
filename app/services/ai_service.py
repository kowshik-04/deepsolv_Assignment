import asyncio
import json
import logging
from typing import Dict, Any

from openai import OpenAI
from app.config import settings

logger = logging.getLogger(__name__)


class AIService:

    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY not configured")

        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate_page_insights(self, page: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""
Analyze the LinkedIn company data below and generate business insights.

Company Name: {page.get('name')}
Industry: {page.get('industry')}
Followers: {page.get('followers')}
Employees: {page.get('head_count')}
Description: {page.get('description')}
Specialties: {page.get('specialties')}
"""

        def _call_openai():
            return self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a senior market analyst. Respond only with valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.2,
            )

        # Run blocking client in a thread to avoid blocking the event loop
        response = await asyncio.to_thread(_call_openai)
        return json.loads(response.choices[0].message.content)
