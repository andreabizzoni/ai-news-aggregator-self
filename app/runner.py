from models import RunnerConfig, RunnerResult
from scrapers import AnthropicAIScraper, YouTubeScraper, OpenAIScraper
from db import Repository
from agent import Agent


class Runner:
    def __init__(self, config: RunnerConfig, repository: Repository):
        self.time_window_hours = config.time_window_hours
        self.youtube_channels = config.youtube_channels
        self.repository = repository
        self.agent = Agent()

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

        digested_articles = self.agent.add_digest(all_articles)
        digested_youtube_videos = self.agent.add_digest(youtube_videos)

        videos_saved = self.repository.save_news_items(digested_youtube_videos)
        articles_saved = self.repository.save_news_items(digested_articles)

        return RunnerResult(
            youtube_videos=digested_youtube_videos,
            videos_saved=videos_saved,
            articles=digested_articles,
            articles_saved=articles_saved,
        )


if __name__ == "__main__":
    repository = Repository()
    repository.create_tables()

    config = RunnerConfig(
        time_window_hours=100,
        youtube_channels=["UCLKPca3kwwd-B59HNr-_lvA", "UCn8ujwUInbJkBhffxqAPBVQ"],
    )
    runner = Runner(config, repository)
    result = runner.run()
    print("\nScraping completed successfully!")
    print(f"YouTube videos: {result.videos_saved}")
    print(f"Articles: {result.articles_saved}")
