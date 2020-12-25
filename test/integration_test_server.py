import requests

base_url = 'http://0.0.0.0:5000'


def test_get_invalid_key():
    r = requests.get(base_url+'/ab')
    # not this key in cache or DB, assert 404 not Found
    assert r.status_code == 404


def test_create_read_delete():
    # create an item with key='ab', value='cd'
    r = requests.post(base_url, {"key": "ab", "value": "cd"})
    assert r.status_code == 201

    r = requests.get(base_url + '/ab')
    # Found, return status code 200
    assert r.status_code == 200

    # delete the element
    r = requests.delete(base_url + '/ab')
    assert r.status_code == 200

    # get after delete, should return 404
    r = requests.get(base_url + '/ab')
    assert r.status_code == 404


def test_crud_whole_flow():
    r = requests.get(base_url + '/ab')
    assert r.status_code == 404

    r = requests.put(base_url, {"key": "ab", "value": "ef"})
    assert r.status_code == 400

    r = requests.post(base_url, {"key": "ab"})
    assert r.status_code == 400

    r = requests.post(base_url, {"key": "ab", "value": "cd"})
    assert r.status_code == 201

    r = requests.get(base_url + '/ab')
    assert r.status_code == 200
    last_v = r.text

    r = requests.put(base_url, {"key": "ab", "value": "ef"})
    # key exist, update success
    assert r.status_code == 200

    r = requests.get(base_url + '/ab')
    assert r.status_code == 200
    new_v = r.text
    assert last_v != new_v

    r = requests.delete(base_url + '/ab')
    assert r.status_code == 200

    r = requests.get(base_url + '/ab')
    assert r.status_code == 404
