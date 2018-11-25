def test_valid_login_logout(test_client):
    data = {
        'email': 'test@test.com',
        'password': 'testing123'
    }
    response = test_client.post('/userpanel/login', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome testing123" in response.data

    response = test_client.get('/userpanel/logout', follow_redirects=True)
    assert response.status_code == 200
