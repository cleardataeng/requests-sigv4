
# requests-sigv4

Python library for making AWS4-HMAC-SHA256 signed calls with requests.

### Usage
---------

```python
from requests_sigv4 import Sigv4Request

request = Sigv4Request(region="us-west-2")
response = request.get(
    url='{}/pets/1234'.format(API_PATH),
    headers={'X-Custom-Header': 'foo-bar'},
)
```

```python
# Constructor options.
# role_arn can be provided to STS with the current credential context.
Sigv4Request(
  region=None,
  access_key=None,
  secret_key=None,
  session_token=None,
  session_expires=3600,
  profile=None,
  role_arn=None,
  role_session_name='awsrequest',
  service='execute-api')
```

### AWS Credentials
-------------------

In the background, the credential provider being used is from [boto3](https://boto3.amazonaws.com).

Credentials from environment variables and the AWS shared credential file will work in the same manner they do with boto3 and the AWS command line.

More about [boto3 credentials](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html).
