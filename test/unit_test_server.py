import pytest

from main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def test_empty_db(client):
    response = client.get('/ab')
    assert response.status_code == 404


def test_create_read_delete(client):
    # create an item with key='ab', value='cd'
    response = client.post(json={"key": "ab", "value": "cd"})
    assert response.status_code == 201

    response = client.get('/ab')
    assert response.status_code == 200
    # Found, return status code 200

    # delete the element
    response = client.delete('/ab')
    assert response.status_code == 200

    # get after delete, should return 404
    response = client.get('/ab')
    assert response.status_code == 404


def test_crud_whole_flow(client):
    # operation failed due to empty db
    response = client.get('/ab')
    assert response.status_code == 404

    response = client.put(json={"key": "ab", "value": "ef"})
    assert response.status_code == 400

    response = client.post(json={"key": "ab"})
    assert response.status_code == 400

    # create - get - update - get - delete - get
    response = client.post(json={"key": "ab", "value": "cd"})
    assert response.status_code == 201

    response = client.get('/ab')
    assert response.status_code == 200
    result = response.json
    assert isinstance(result, dict)
    assert result['key'] == 'ab'
    assert result['value'] == 'cd'
    last_v = result['value']

    response = client.put(json={"key": "ab", "value": "ef"})
    # key exist, update success
    assert response.status_code == 200

    response = client.get('/ab')
    assert response.status_code == 200
    result = response.json
    assert isinstance(result, dict)
    assert result['key'] == 'ab'
    assert result['value'] == 'ef'
    new_v = result['value']
    assert last_v != new_v

    response = client.delete('/ab')
    assert response.status_code == 200

    response = client.get('/ab')
    assert response.status_code == 404
