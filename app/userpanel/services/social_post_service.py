import random
from typing import List
from typing import NamedTuple

from sqlalchemy import asc

from app.blog.models import Article
from app.database import db

WELCOME_TITLES_LIST = [
    "Hello 👋 Who is looking for a great article to read? Ook. See our latest press and find something for yourself 😉 Full list below 👇💸",
    "Time for new challenges! We have a lot of articles for you. Grab the latest press! 🔥 And for those who do not have time - at the bottom you find the full list👇💪😎",
    "Hello 👋 We come to you with our new press 🔥, below you will find the entire list 👇",
    "👋 A new press from us special for you 😎, we encourage you to read 💪💪💪",
    "Hello 👋! 🤓 Check the latest newspapers in the meantime before brewing your favorite coffee 😉",
    "Hi 👋! 😉 A fresh press came for you, and if you don't have too much time, we recommend that you look at the very end 💪🔥👇",
]

LINK_EMOJI_LIST = ["🌍", "🎯", "🔎", "📍"]

FOOTER = "Beside that we still encourage you to visit our app and check the tools 🔥🔥 https://gene-calc.pl/"


class SocialPost(NamedTuple):
    header: str
    links: List[str]
    footer: str


class SocialPostService:
    def get_articles(self) -> List[Article]:
        articles_to_publish = (
            Article.query.filter_by(was_published=False).order_by(asc(Article.created_at)).limit(10).all()
        )

        for article in articles_to_publish:
            article.was_published = True
            db.session.commit()

        return articles_to_publish

    def generate_title(self) -> str:
        n = random.randint(0, len(WELCOME_TITLES_LIST) - 1)
        return WELCOME_TITLES_LIST[n]

    def generate_emoji(self) -> str:
        n = random.randint(0, len(LINK_EMOJI_LIST) - 1)
        return LINK_EMOJI_LIST[n]

    def generate_links(self) -> list:
        articles_to_publish = self.get_articles()
        emoji = self.generate_emoji()

        links = [f'{emoji} {article.title}: {article.link}' for article in articles_to_publish]
        return links

    def generate_post(self) -> SocialPost:
        title = self.generate_title()
        links = self.generate_links()

        return SocialPost(header=title, links=links, footer=FOOTER)
