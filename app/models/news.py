"""News article models."""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Literal


class NewsArticle(BaseModel):
    """Represents a news article."""

    source: Literal["OpenAI", "Anthropic"] = Field(
        description="The source of the news article"
    )
    title: str = Field(..., description="The title of the news article")
    description: str = Field(
        ..., description="The description or summary of the article"
    )
    url: str = Field(..., description="The URL to the full article")
    published_at: datetime = Field(..., description="The publication date and time")
    guid: str = Field(..., description="The globally unique identifier for the article")
