import datetime
from typing import List
from typing import Tuple

import feedparser
from feedparser import FeedParserDict
from flask import flash

from app.blog.models import Article
from app.blog.models import Feed
from app.database import db


class BlogAggregatorService:
    @staticmethod
    def parse_pub_date(entry_pub_date: tuple) -> datetime.datetime:
        return datetime.datetime(*(entry_pub_date[0:6]))

    @staticmethod
    def parse_single_entry(entry: FeedParserDict) -> Article:
        article = Article()
        article.title = entry.get('title')
        article.link = entry.get('link')
        article.pub_date = BlogAggregatorService.parse_pub_date(entry.get('published_parsed'))
        article.desc = entry.get('summary')

        return article

    @staticmethod
    def parse_feed(feed_url: str) -> List[FeedParserDict]:
        response = feedparser.parse(feed_url)

        return response.get('entries')

    @staticmethod
    def validate_feed(feed_url: str) -> Tuple[bool, str]:
        parsed_feed = BlogAggregatorService.parse_feed(feed_url)

        for entry in parsed_feed:
            pub_date = BlogAggregatorService.parse_pub_date(entry.published_parsed)

            if pub_date.year < 2018:
                return False, 'This feed contain post with publication date older than 2018'

            if '<div>' in entry.get('summary'):
                return False, 'This feed contain HTML in summary tag'

        return True, 'ok'

    @staticmethod
    def aggregate() -> None:
        objects_to_add = []

        feed_list = Feed.query.all()

        for feed in feed_list:
            parsed_feed = BlogAggregatorService.parse_feed(feed.url)

            for entry in parsed_feed:
                article = BlogAggregatorService.parse_single_entry(entry)

                if not Article.query.filter_by(link=article.link).first():
                    flash(f'Successfully added article - {article.title}', 'info')
                    objects_to_add.append(article)

        db.session.add_all(objects_to_add)
        db.session.commit()

        if len(objects_to_add):
            flash(f'You have successfully added {len(objects_to_add)} articles', 'success')
        else:
            flash(f'Blog aggregator successfully run but without any new articles', 'info')
