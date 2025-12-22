"""YouTube video models."""

from datetime import datetime
from pydantic import BaseModel, Field


class YouTubeVideo(BaseModel):
    """Represents a YouTube video."""

    video_id: str = Field(..., description="The unique YouTube video ID")
    title: str = Field(..., description="The title of the video")
    url: str = Field(..., description="The URL to the video")
    published_at: datetime = Field(..., description="The publication date and time")
    author: str = Field(..., description="The author/channel name of the video")
    transcript: str = Field(
        default=None, description="The full transcript text of the video"
    )
