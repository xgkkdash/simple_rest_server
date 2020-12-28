import requests

base_url = 'http://0.0.0.0:5000'


def test_using_token_for_auth():
    login_url = base_url + '/login'
    r = requests.post(login_url, auth=("root", "root"))
    assert r.status_code == 200
    token = r.content.decode("utf-8")

    access_url = base_url + '/protected'
    headers = {"Authorization": token}
    r = requests.get(access_url, headers=headers)
    assert r.status_code == 200


if __name__ == '__main__':
    test_using_token_for_auth()
