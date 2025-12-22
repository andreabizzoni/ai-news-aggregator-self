from pydantic import BaseModel, Field
from typing import List


class Digest(BaseModel):
    """Represents a news item digest"""

    guid: str = Field(..., description="The globally unique identifier for the item")
    digest: str = Field(..., description="The digest for the item")


class LLMResponse(BaseModel):
    """Represents a structured LLM response"""

    digests: List[Digest] = Field(..., description="A list of digests")
