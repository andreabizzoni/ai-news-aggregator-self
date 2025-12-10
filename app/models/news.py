"""News article models."""

from datetime import datetime
from pydantic import BaseModel, Field


class NewsArticle(BaseModel):
    """Represents a news article."""

    title: str = Field(..., description="The title of the news article")
    description: str = Field(
        ..., description="The description or summary of the article"
    )
    url: str = Field(..., description="The URL to the full article")
    published_at: datetime = Field(..., description="The publication date and time")
    guid: str = Field(..., description="The globally unique identifier for the article")
