from models import RunnerConfig, RunnerResult
from scrapers import AnthropicAIScraper, YouTubeScraper, OpenAIScraper
from db import Repository


class Runner:
    def __init__(self, config: RunnerConfig, repository: Repository):
        self.time_window_hours = config.time_window_hours
        self.youtube_channels = config.youtube_channels
        self.repository = repository

    def run(self):
        youtube_scraper = YouTubeScraper()
        openai_scraper = OpenAIScraper()
        anthropic_scraper = AnthropicAIScraper()

        youtube_videos = []
        for channel in self.youtube_channels:
            youtube_videos.extend(
                youtube_scraper.scrape_youtube_channel(channel, self.time_window_hours)
            )

        openai_articles = openai_scraper.scrape_news(self.time_window_hours)
        anthropic_articles = anthropic_scraper.scrape_news(self.time_window_hours)

        all_articles = openai_articles + anthropic_articles
        videos_saved = self.repository.save_youtube_videos(youtube_videos)
        articles_saved = self.repository.save_news_articles(all_articles)

        print(f"Saved {videos_saved} videos and {articles_saved} articles to database")

        return RunnerResult(
            youtube_videos=youtube_videos,
            openai_articles=openai_articles,
            anthropic_articles=anthropic_articles,
        )


if __name__ == "__main__":
    repository = Repository()
    repository.create_tables()

    config = RunnerConfig(
        time_window_hours=200,
        youtube_channels=["UCLKPca3kwwd-B59HNr-_lvA", "UCn8ujwUInbJkBhffxqAPBVQ"],
    )
    runner = Runner(config, repository)
    result = runner.run()
    print("\nScraping completed successfully!")
    print(f"YouTube videos: {len(result.youtube_videos)}")
    print(f"OpenAI articles: {len(result.openai_articles)}")
    print(f"Anthropic articles: {len(result.anthropic_articles)}")
