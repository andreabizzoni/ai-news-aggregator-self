"""Database repository for managing database operations."""

import os
from typing import List
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert

from .models import Base, YouTubeVideoDB, NewsArticleDB
from models.news import NewsArticle
from models.youtube import YouTubeVideo

load_dotenv()


class Repository:
    """Repository for database operations."""

    def __init__(self, database_url: str | None = None):
        """Initialize the repository with a database connection.

        Args:
            database_url: Database connection URL. If not provided, reads from DATABASE_URL env var.
        """
        self.database_url = database_url or os.getenv("DATABASE_URL")
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Create all database tables."""
        Base.metadata.create_all(self.engine)

    def save_youtube_videos(self, videos: List[YouTubeVideo]) -> int:
        """Save YouTube videos to the database, ignoring duplicates.

        Args:
            videos: List of YouTube videos to save.

        Returns:
            Number of videos saved.
        """
        if not videos:
            return 0

        with self.SessionLocal() as session:
            for video in videos:
                stmt = insert(YouTubeVideoDB).values(
                    video_id=video.video_id,
                    title=video.title,
                    url=video.url,
                    published_at=video.published_at,
                    author=video.author,
                    transcript=video.transcript,
                )
                stmt = stmt.on_conflict_do_nothing(index_elements=["video_id"])
                session.execute(stmt)

            session.commit()
            return len(videos)

    def save_news_articles(self, articles: List[NewsArticle]) -> int:
        """Save news articles to the database using upsert.

        Args:
            articles: List of news articles to save.

        Returns:
            Number of articles saved.
        """
        if not articles:
            return 0

        with self.SessionLocal() as session:
            for article in articles:
                stmt = insert(NewsArticleDB).values(
                    source=article.source,
                    title=article.title,
                    description=article.description,
                    url=article.url,
                    published_at=article.published_at,
                    guid=article.guid,
                )
                stmt = stmt.on_conflict_do_nothing(index_elements=["guid"])
                session.execute(stmt)

            session.commit()
            return len(articles)

    def get_all_youtube_videos(self) -> List[YouTubeVideoDB]:
        """Retrieve all YouTube videos from the database."""
        with self.SessionLocal() as session:
            return session.query(YouTubeVideoDB).all()

    def get_all_news_articles(self) -> List[NewsArticleDB]:
        """Retrieve all news articles from the database."""
        with self.SessionLocal() as session:
            return session.query(NewsArticleDB).all()
