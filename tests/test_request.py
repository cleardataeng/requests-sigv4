import json

import pytest
import requests_sigv4

API_REGION = 'us-west-2'
# PetStore mock API Gateway
API_PATH = "https://znlmeqqrf5.execute-api.us-west-2.amazonaws.com/testing"
API_HEADERS = {
    'Accept': 'application/json',
    'Content-type': 'application/json',
    'x-foo': 'bar',
}


def test_get():
    req = requests_sigv4.requests.Sigv4Request(region=API_REGION)
    got = req.options(
        url='{}/pets'.format(API_PATH),
        headers=API_HEADERS,
    )
    assert got.status_code == 200


@pytest.mark.integration
def test_get_integration():
    req = requests_sigv4.requests.Sigv4Request(region=API_REGION)
    got = req.get(
        url='{}/pets/1234'.format(API_PATH),
        headers=API_HEADERS,
    )
    c = json.loads(got.content.decode('utf-8'))
    print(c)
    assert (
        got.status_code == 200
        or 'not authorized' in c.get('message', '')
        or 'not authorized' in c.get('Message', '')
    )
