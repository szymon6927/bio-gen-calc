def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200

def test_about_page(test_client):
    response = test_client.get('/about')
    assert response.status_code == 200

def test_hw_page(test_client):
    response = test_client.get('/hardy-weinber-page')
    assert response.status_code == 200

def test_chi_square_page(test_client):
    response = test_client.get('/chi-square-page')
    assert response.status_code == 200

def test_pic_page(test_client):
    response = test_client.get('/pic')
    assert response.status_code == 200

def test_genetic_distance_page(test_client):
    response = test_client.get('/genetic-distance')
    assert response.status_code == 200

def test_contact_page(test_client):
    response = test_client.get('/contact')
    assert response.status_code == 200