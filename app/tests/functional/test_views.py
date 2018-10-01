def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Gene-Calc' in response.data


def test_about_page(test_client):
    response = test_client.get('/about')
    assert response.status_code == 200
    assert b'Materials' in response.data


def test_hw_page(test_client):
    response = test_client.get('/hardy-weinber-page')
    assert response.status_code == 200
    assert b'Hardy-Weinberg equilibrium' in response.data


def test_chi_square_page(test_client):
    response = test_client.get('/chi-square-page')
    assert response.status_code == 200
    assert b'Chi-Square tests' in response.data


def test_pic_page(test_client):
    response = test_client.get('/pic')
    assert response.status_code == 200
    assert b'Polymorphic Information Content (PIC) and Heterozygosity (H).' in response.data


def test_genetic_distance_page(test_client):
    response = test_client.get('/genetic-distance')
    assert response.status_code == 200
    assert b'Genetic Distance' in response.data


def test_contact_page(test_client):
    response = test_client.get('/contact')
    assert response.status_code == 200
    assert b'Contact Us' in response.data


def test_donors_page(test_client):
    response = test_client.get('/donors')
    assert response.status_code == 200
    assert b'Our donors' in response.data


def test_dotplot_page(test_client):
    response = test_client.get('/sequences-analysis-tools/dot-plot')
    assert response.status_code == 200
    assert b'Dot plot' in response.data


def test_consensus_sequence_page(test_client):
    response = test_client.get('/sequences-analysis-tools/consensus-sequence')
    assert response.status_code == 200
    assert b'Consensus Sequence' in response.data


def test_sequences_tools_page(test_client):
    response = test_client.get('/sequences-analysis-tools/sequences-tools')
    assert response.status_code == 200
    assert b'Sequences Tools' in response.data

def test_robots_page(test_client):
    response = test_client.get('/robots.txt')
    assert response.status_code == 200
    assert b'User-Agent: *' in response.data

def test_sitemap_page(test_client):
    response = test_client.get('/sitemap.xml')
    assert response.status_code == 200