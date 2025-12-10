"""Pydantic models for the AI news aggregator."""

from .news import NewsArticle
from .youtube import YouTubeVideo, VideoTranscript

__all__ = ["NewsArticle", "YouTubeVideo", "VideoTranscript"]
