from typing import NamedTuple
from unittest.mock import patch

import pytest

from app.userpanel.services.social_post_service import FOOTER
from app.userpanel.services.social_post_service import LINK_EMOJI_LIST
from app.userpanel.services.social_post_service import WELCOME_TITLES_LIST
from app.userpanel.services.social_post_service import SocialPost
from app.userpanel.services.social_post_service import SocialPostService


class FakeArticle(NamedTuple):
    title: str
    link: str


@pytest.fixture
def fake_articles():
    article_list = []
    for i in range(5):
        article = FakeArticle(title=f'test_title_{i}', link=f'test_link_{i}')

        article_list.append(article)

    return article_list


def test_social_post_service_generate_title():
    social_post_service = SocialPostService()
    title = social_post_service.generate_title()

    assert title in WELCOME_TITLES_LIST


def test_social_post_service_generate_emoji():
    social_post_service = SocialPostService()
    emoji = social_post_service.generate_emoji()

    assert emoji in LINK_EMOJI_LIST


@patch.object(SocialPostService, 'get_articles')
def test_social_post_service_generate_links(get_articles_mock, fake_articles):
    get_articles_mock.return_value = fake_articles

    social_post_service = SocialPostService()
    links = social_post_service.generate_links()

    assert isinstance(links, list)
    assert len(links) == 5
    assert 'test' in links[0]


@patch.object(SocialPostService, 'get_articles')
def test_social_post_service_generate_post(get_articles_mock, fake_articles):
    get_articles_mock.return_value = fake_articles

    social_post_service = SocialPostService()
    post = social_post_service.generate_post()

    assert isinstance(post, SocialPost)
    assert post.footer == FOOTER
    assert isinstance(post.links, list)
    assert 'test' in post.links[0]
