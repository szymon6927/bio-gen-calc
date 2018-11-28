def test_valid_login_logout(test_client, init_db):
    data = {
        "login_or_email": "test2@test.com",
        "password": "testing321"
    }

    response = test_client.post('/userpanel/login', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b"Invalid username or password" not in response.data
    assert b"Welcome" in response.data


def test_invalid_login_logout(test_client, init_db):
    data = {
        "login_or_email": "test2@test.com",
        "password": "testing321321"
    }

    response = test_client.post('/userpanel/login', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b"Invalid username or password" in response.data
