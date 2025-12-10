"""YouTube channel scraper using RSS feed."""

from datetime import datetime, timedelta, timezone
from typing import List
import feedparser
from youtube_transcript_api import YouTubeTranscriptApi

from models.youtube import YouTubeVideo, VideoTranscript


class YouTubeScraper:
    """Scrapes YouTube channel RSS feeds for recent videos."""

    RSS_FEED_URL = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

    def get_latest_videos(
        self, channel_id: str, time_window_hours: int = 24
    ) -> list[YouTubeVideo]:
        """
        Scrape a YouTube channel for videos published within a time window.

        Args:
            channel_id: The YouTube channel ID
            time_window_hours: Number of hours to look back (default: 24)

        Returns:
            List of YouTubeVideo objects published within the time window
        """
        feed_url = self.RSS_FEED_URL.format(channel_id=channel_id)
        feed = feedparser.parse(feed_url)

        if not feed.entries:
            return []

        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=time_window_hours)
        videos = []

        for entry in feed.entries:
            published_at = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

            if published_at >= cutoff_time:
                video = YouTubeVideo(
                    video_id=entry.yt_videoid,
                    title=entry.title,
                    url=entry.link,
                    published_at=published_at,
                    author=entry.author,
                    thumbnail_url=entry.media_thumbnail[0]["url"]
                    if entry.get("media_thumbnail")
                    else None,
                )
                videos.append(video)

        return videos

    def get_transcript(self, video_id: str) -> VideoTranscript:
        """
        Fetch the transcript for a YouTube video.

        Args:
            video_id: The YouTube video ID

        Returns:
            The full transcript as a string
        """
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.fetch(video_id)
        return VideoTranscript(
            transcript=" ".join([snippet.text for snippet in transcript_list])
        )

    def scrape_youtube_channel(
        self, channel_id: str, time_window_hours: int = 24
    ) -> List[VideoTranscript]:
        videos = self.get_latest_videos(channel_id, time_window_hours)
        transcripts = []
        for video in videos:
            transcripts.append(scraper.get_transcript(video.video_id))
        return transcripts


if __name__ == "__main__":
    scraper = YouTubeScraper()
    print(scraper.scrape_youtube_channel("UCHnyfMqiRRG1u-2MsSQLbXA", 100))
