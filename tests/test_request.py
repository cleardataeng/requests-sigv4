import json

import pytest  # noqa: F401
from requests_sigv4 import Sigv4Request

API_REGION = 'us-west-2'
# PetStore mock API Gateway
API_PATH = "https://znlmeqqrf5.execute-api.us-west-2.amazonaws.com/testing"
API_HEADERS = {
    'Accept': 'application/json',
    'Content-type': 'application/json',
    'x-foo': 'bar',
}


def test_get():
    req = Sigv4Request(region=API_REGION)
    got = req.options(
        url='{}/pets'.format(API_PATH),
        params={
            'foo': 'boo boo'
        },
        headers=API_HEADERS,
    )
    assert got.status_code == 200


def test_get_query_space():
    req = Sigv4Request(region=API_REGION)
    res = req.get(
        url="https://httpbin.org/get",
        params={
            "foo": "bar bar",
        },
        headers=API_HEADERS
    )
    got = json.loads(res.content.decode('utf-8'))
    assert got['url'] == 'https://httpbin.org/get?foo=bar bar'


def test_get_integration():
    req = Sigv4Request(region=API_REGION)
    got = req.get(
        url='{}/pets/1234'.format(API_PATH),
        headers=API_HEADERS,
    )
    c = json.loads(got.content.decode('utf-8'))
    assert (
        got.status_code == 200
        or 'not authorized' in c.get('message', '')
        or 'not authorized' in c.get('Message', '')
    )
