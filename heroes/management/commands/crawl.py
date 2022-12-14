from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import defer

from heroes_scraper.spiders.heroes_spyder import (
    TownScraper,
    CreatureScraper,
    SpellScraper,
    SecondarySkillScraper,
    ClassScraper,
    ResourceScraper,
    HeroScraper,
)


class Command(BaseCommand):
    help = "Release the spiders"

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())

        @defer.inlineCallbacks
        def crawl(process):
            yield process.crawl(TownScraper)
            yield process.crawl(CreatureScraper)
            yield process.crawl(SpellScraper)
            yield process.crawl(SecondarySkillScraper)
            yield process.crawl(ClassScraper)
            yield process.crawl(ResourceScraper)
            yield process.crawl(HeroScraper)

        crawl(process)
        process.start()
