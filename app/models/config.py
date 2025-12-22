from pydantic import BaseModel, Field
from typing import List

from .news import NewsItem


class RunnerConfig(BaseModel):
    time_window_hours: int = Field(
        default=24, description="The time window scrapers run for"
    )
    youtube_channels: List[str] = Field(
        default=None, description="The list of channel ID's to scrape"
    )


class RunnerResult(BaseModel):
    youtube_videos: List[NewsItem] = Field(
        default=None, description="List of youtube videos"
    )
    videos_saved: int = Field(default=0, description="Number of YouTube videos saved")
    articles: List[NewsItem] = Field(default=None, description="List of news articles")
    articles_saved: int = Field(default=0, description="Number of news articles saved")
