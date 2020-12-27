import requests

base_url = 'http://0.0.0.0:5000'


def test_unauthorized():
    r = requests.get(base_url)
    # Unauthorized Access, 401
    assert r.status_code == 401


def test_authenticated():
    r = requests.get(base_url, auth=("root", "root"))
    # authenticate success, 200
    assert r.status_code == 200
