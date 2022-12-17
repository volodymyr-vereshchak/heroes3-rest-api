from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from heroes_scraper.spiders.heroes_spyder import(
    TownScraper,
    CreatureScraper,
    SpellScraper,
    SecondarySkillScraper,
    ClassScraper
)


class Command(BaseCommand):
    help = "Release the spiders"

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())

        process.crawl(TownScraper)
        process.crawl(CreatureScraper)
        process.crawl(SpellScraper)
        process.crawl(SecondarySkillScraper)
        process.crawl(ClassScraper)
        process.start()