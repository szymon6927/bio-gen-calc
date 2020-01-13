from unittest.mock import patch

import pytest

from app.blog.models import Article
from app.blog.models import Feed
from tests.integration.constants import URL
from tests.integration.utils import create_customer
from tests.integration.utils import create_superuser_customer
from tests.integration.utils import get_fixture
from tests.integration.utils import login_customer


@pytest.fixture
def fake_feedparser_entries():
    feed_parser_object = [
        {
            'title': 'Test Article Title 1',
            'link': 'http://www.test-article-url.com/article/1',
            'published_parsed': (2020, 1, 9, 7, 46, 22),
            'summary': 'Test Article Summary 1',
        },
        {
            'title': 'Test Article Title 2',
            'link': 'http://www.test-article-url.com/article/2',
            'published_parsed': (2020, 1, 10, 7, 46, 22),
            'summary': 'Test Article Summary 2',
        },
    ]

    return feed_parser_object


@patch('app.userpanel.services.blog_aggregator_service.BlogAggregatorService.parse_feed')
def test_get_aggregator_run_view_superuser(parse_feed_mock, fake_feedparser_entries, test_client):
    parse_feed_mock.return_value = fake_feedparser_entries

    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_RUN_AGGREGATOR, follow_redirects=True)

    number_of_feeds = len(Feed.query.all())
    number_of_articles = len(fake_feedparser_entries)

    assert response.status_code == 200
    assert b'Articles' in response.data
    assert b'Successfully added article' in response.data
    assert f'You have successfully added {number_of_feeds * number_of_articles} articles' in response.data.decode()


def test_get_aggregator_run_view_normal_customer(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_RUN_AGGREGATOR, follow_redirects=True)

    assert response.status_code == 200
    assert b'You do not have access here!' in response.data


def test_post_aggregator_run_view(test_client):
    response = test_client.post(URL.USERPANEL_RUN_AGGREGATOR)

    assert response.status_code == 405
    assert b'Method Not Allowed' in response.data


def test_get_generate_social_post_view_superuser(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_GENERATE_SOCIAL_POST, follow_redirects=True)

    articles_to_publish = Article.query.filter_by(was_published=False).all()

    assert response.status_code == 200
    assert b'Generated social media post' in response.data

    articles_fixture = get_fixture('blog_aggregator_articles.json')
    for article_fixture in articles_fixture:
        assert f"{article_fixture.get('title')}" in response.data.decode()
        assert f"{article_fixture.get('link')}" in response.data.decode()

    assert len(articles_to_publish) == 0


def test_get_generate_social_post_view_normal_customer(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_GENERATE_SOCIAL_POST, follow_redirects=True)

    assert response.status_code == 200
    assert b'You do not have access here!' in response.data


def test_post_generate_social_post_view(test_client):
    response = test_client.post(URL.USERPANEL_GENERATE_SOCIAL_POST)

    assert response.status_code == 405
    assert b'Method Not Allowed' in response.data


def test_get_feeds_view_superuser(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_FEEDS_ALL)

    assert b'Feed list' in response.data
    assert b'Feed 1' in response.data
    assert b'Feed 2' in response.data


def test_get_feeds_view_normal_customer(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_FEEDS_ALL)

    assert response.status_code == 200
    assert b'You do not have access here!' in response.data


def test_get_add_feed_superuser(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.post(URL.USERPANEL_FEED_ADD)

    assert response.status_code == 200
    assert b'Add new feed' in response.data


def test_get_add_feed_normal_customer(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.post(URL.USERPANEL_FEED_ADD)

    assert response.status_code == 200
    assert b'You do not have access here!' in response.data


@patch('app.userpanel.services.blog_aggregator_service.BlogAggregatorService.validate_feed')
@patch('app.userpanel.forms.requests.get')
def test_post_add_feed(mock_get, mock_validate_feed, test_client):
    mock_get.return_value.status_code = 200
    mock_validate_feed.return_value = True, 'ok'

    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    data = {'name': 'Test feed name', 'url': 'http://www.test-url.com/feed/'}
    response = test_client.post(URL.USERPANEL_FEED_ADD, data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'You have successfully added the feed' in response.data


@patch('app.userpanel.forms.requests.get')
def test_post_add_feed_with_wrong_url_where_url_is_not_working(mock_get, test_client):
    mock_get.return_value.status_code = 404

    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    data = {'name': 'Test feed name', 'url': 'http://www.test-url.com/feed/'}
    response = test_client.post(URL.USERPANEL_FEED_ADD, data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'Feed with this URL return status code different than 200' in response.data


@patch('app.userpanel.forms.requests.get')
def test_post_add_feed_with_url_which_already_exists(mock_get, test_client):
    mock_get.return_value.status_code = 200

    feed_which_already_exist = Feed.query.filter_by(id=1).first()

    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    data = {'name': 'Test feed name', 'url': feed_which_already_exist.url}
    response = test_client.post(URL.USERPANEL_FEED_ADD, data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'Feed with this URL already exist' in response.data


@patch('app.userpanel.services.blog_aggregator_service.BlogAggregatorService.validate_feed')
@patch('app.userpanel.forms.requests.get')
def test_post_add_feed_with_wrong_url_where_posts_are_old(mock_get, mock_validate_feed, test_client):
    mock_get.return_value.status_code = 200
    mock_validate_feed.return_value = False, 'This feed contain post with publication date older than 2018'

    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    data = {'url': 'http://www.test-url.com/feed/'}
    response = test_client.post(URL.USERPANEL_FEED_ADD, data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'This feed contain post with publication date older than 2018' in response.data


@patch('app.userpanel.services.blog_aggregator_service.BlogAggregatorService.validate_feed')
@patch('app.userpanel.forms.requests.get')
def test_post_add_feed_where_feed_summary_tag_contains_html(mock_get, mock_validate_feed, test_client):
    mock_get.return_value.status_code = 200
    mock_validate_feed.return_value = False, 'This feed contain HTML in summary tag'

    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    data = {'url': 'http://www.test-url.com/feed/'}
    response = test_client.post(URL.USERPANEL_FEED_ADD, data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'This feed contain HTML in summary tag' in response.data


def test_get_feed_details_view_superuser(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    feeds_fixture = get_fixture('blog_aggregator_feeds.json')

    for feed_fixture in feeds_fixture:
        response = test_client.get(f"{URL.USERPANEL_FEED_DETAILS}{feed_fixture.get('id')}")

        assert response.status_code == 200
        assert b'Edit feed' in response.data
        assert f"{feed_fixture.get('name')}" in response.data.decode()
        assert f"{feed_fixture.get('url')}" in response.data.decode()


def test_get_feed_details_view_normal_customer(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    feeds_fixture = get_fixture('blog_aggregator_feeds.json')

    for feed_fixture in feeds_fixture:
        response = test_client.get(f"{URL.USERPANEL_FEED_DETAILS}{feed_fixture.get('id')}")

        assert b'You do not have access here!' in response.data


@patch('app.userpanel.services.blog_aggregator_service.BlogAggregatorService.validate_feed')
@patch('app.userpanel.forms.requests.get')
def test_post_feed_details_view(mock_get, mock_validate_feed, test_client):
    mock_get.return_value.status_code = 200
    mock_validate_feed.return_value = True, 'ok'

    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    feeds_fixture = get_fixture('blog_aggregator_feeds.json')

    for i, feed_fixture in enumerate(feeds_fixture):
        data = dict()
        data['name'] = f"Test Feed Name {i} - changed"

        response = test_client.post(
            f"{URL.USERPANEL_FEED_DETAILS}{feed_fixture.get('id')}", data=data, follow_redirects=True
        )

        assert response.status_code == 200
        assert b'You have successfully edited the feed' in response.data


def test_get_feed_delete_view(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    feeds_fixture = get_fixture('blog_aggregator_feeds.json')

    for i, feed_fixture in enumerate(feeds_fixture):
        response = test_client.get(f"{URL.USERPANEL_FEED_DELETE}{feed_fixture.get('id')}", follow_redirects=True)

        assert response.status_code == 200
        assert b'You have successfully delete the feed' in response.data


def test_get_all_articles_super_user(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_ARTICLES_ALL)

    assert response.status_code == 200
    assert b'Articles' in response.data


def test_get_all_articles_normal_customer(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_ARTICLES_ALL)

    assert response.status_code == 200
    assert b'You do not have access here!' in response.data


def test_get_add_article_superuser(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_ARTICLE_ADD)

    assert response.status_code == 200
    assert b'Add new article' in response.data


def test_get_add_article_normal_customer(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_ARTICLE_ADD)

    assert response.status_code == 200
    assert b'You do not have access here!' in response.data


def test_post_add_article(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    data = {
        'title': 'Test Article Title',
        'link': 'http://www.test-article.com/link',
        'pub_date': '2020-01-10 06:00:00',
        'desc': 'Test Article Description',
        'was_published': False,
    }

    response = test_client.post(URL.USERPANEL_ARTICLE_ADD, data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'You have successfully added the article' in response.data


def test_get_article_details_view_superuser(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    articles_fixture = get_fixture('blog_aggregator_articles.json')

    for article_fixture in articles_fixture:
        response = test_client.get(f"{URL.USERPANEL_ARTICLE_DETAILS}{article_fixture.get('id')}")

        assert response.status_code == 200
        assert b'Edit article' in response.data
        assert f"{article_fixture.get('title')}" in response.data.decode()
        assert f"{article_fixture.get('link')}" in response.data.decode()


def test_get_article_details_view_normal_customer(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    articles_fixture = get_fixture('blog_aggregator_articles.json')

    for article_fixture in articles_fixture:
        response = test_client.get(f"{URL.USERPANEL_ARTICLE_DETAILS}{article_fixture.get('id')}")

        assert b'You do not have access here!' in response.data


def test_post_article_details_view(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    articles_fixture = get_fixture('blog_aggregator_articles.json')

    for i, article_fixture in enumerate(articles_fixture):
        data = dict()
        data['title'] = article_fixture.get('title')
        data['pub_date'] = article_fixture.get('pub_date')
        data['desc'] = f"test-publication-desc-{i}"

        response = test_client.post(
            f"{URL.USERPANEL_ARTICLE_DETAILS}{article_fixture.get('id')}", data=data, follow_redirects=True
        )

        assert response.status_code == 200
        assert b'You have successfully edited the article' in response.data


def test_get_article_delete_view(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    articles_fixture = get_fixture('blog_aggregator_articles.json')

    for article_fixture in articles_fixture:
        response = test_client.get(f"{URL.USERPANEL_ARTICLE_DELETE}{article_fixture.get('id')}", follow_redirects=True)

        assert response.status_code == 200
        assert b'You have successfully delete the article' in response.data
