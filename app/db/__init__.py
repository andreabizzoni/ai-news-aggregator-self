"""Database module for storing scraped content."""

from .models import Base, NewsItemDB
from .repository import Repository

__all__ = ["Base", "NewsItemDB", "Repository"]
