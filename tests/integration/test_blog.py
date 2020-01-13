from tests.integration.constants import URL


def test_get_blog_ok(test_client):
    response = test_client.get(URL.BLOG_GET)

    assert response.status_code == 200
    assert b'Blog' in response.data


def test_get_blog_pagination_ok(test_client):
    response = test_client.get(f'{URL.BLOG_GET}?page=2')

    assert response.status_code == 200
    assert b'Blog' in response.data


def test_get_blog_pagination_wrong(test_client):
    response = test_client.get(f'{URL.BLOG_GET}?page=xxx')

    assert response.status_code == 200
    assert b'Blog' in response.data
