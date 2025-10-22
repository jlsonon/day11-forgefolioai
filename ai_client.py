"""
Deprecated: This file previously provided an Anthropic/Groq switch. 
The project now uses Groq exclusively. This stub remains to avoid import errors.
"""

from typing import Dict, Any
from groq_client import GroqClient


class AIClient:
    def __init__(self):
        self.client = GroqClient()

    def generate_portfolio(self, user_data: Dict[str, Any], template_id: str | None = None) -> Dict[str, Any]:
        return self.client.generate_portfolio(user_data, template_id)
