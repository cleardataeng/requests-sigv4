import requests
import boto3

from requests_aws_sign import AWSV4Sign


class Sigv4Request(object):
    def __init__(
            self, region=None, access_key=None, secret_key=None,
            session_token=None, session_expires=3600,
            role_arn=None, role_session_name='awsrequest',
            service='execute-api',
            profile=None,):
        '''Sigv4Request constructor
            region (str, optional): Defaults to None.
                region for session (AWS_DEFAULT_REGION)
            access_key (str, optional): Defaults to None.
                aws access key (AWS_ACCESS_KEY_ID)
            secret_key (str, optional): Defaults to None.
                aws secret access key (AWS_SECRET_ACCESS_KEY)
            session_token (str, optional): Defaults to None.
                aws session token from STS session (AWS_SESSION_TOKEN)
            session_expires (int, optional): Defaults to 3600.
                session expiration in seconds, applies only with role_arn
            role_arn (str, optional): Defaults to None.
                role arn for sts impersonation
            role_session_name (str, optional): Defaults to 'awsrequest'.
                name for sts session, used with role_arn
            service (str, optional): Defaults to 'execute-api'.
                aws service for credential
            profile (str, optional): Defaults to None.
                profile from aws shared configuration file
        '''

        self.creds = None
        self.service = service
        self.region = region

        session = boto3.session.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=session_token,
            region_name=region,
            profile_name=profile,
        )

        if role_arn:
            sts = session.client('sts')
            ar = sts.assume_role(
                RoleArn=role_arn,
                RoleSessionName=role_session_name,
                DurationSeconds=session_expires,
            )
            session = boto3.session.Session(
                aws_access_key_id=ar['Credentials']['AccessKeyId'],
                aws_secret_access_key=ar['Credentials']['SecretAccessKey'],
                aws_session_token=ar['Credentials']['SessionToken'],
                region_name=region,
            )

        self.creds = session.get_credentials()
        if not self.region:
            self.region = session.region_name

    def request(self, method, url,
                params=None,
                data=None,
                headers=None,
                cookies=None,
                files=None,
                timeout=None,
                allow_redirects=True,
                proxies=None,
                hooks=None,
                stream=None,
                verify=True,
                cert=None,
                json=None):
        """Constructs and sends a :class:`Request <Request>`.
        :param method: method for the new :class:`Request` object.
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary or bytes to be sent in the
            query string for the :class:`Request`.
        :param data: (optional) Dictionary, bytes, or file-like object to
            send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of
            the :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send
            with the :class:`Request`.
        :param cookies: (optional) Dict or CookieJar object to send
            with the :class:`Request`.
        :param files: (optional) Dictionary of ``'name': file-like-objects``
            (or ``{'name': ('filename', fileobj)}``) for multipart
            encoding upload.
        :param timeout: (optional) How long to wait for the server to send data
            before giving up, as a float, or a :ref:`(connect timeout, read
            timeout) <timeouts>` tuple.
        :type timeout: float or tuple
        :param allow_redirects: (optional) Boolean. Set to True if
            POST/PUT/DELETE redirect following is allowed.
        :type allow_redirects: bool
        :param proxies: (optional) Dictionary mapping protocol to the
            URL of the proxy.
        :param verify: (optional) if ``True``, the SSL cert will be verified.
            A CA_BUNDLE path can also be provided.
        :param stream: (optional) if ``False``, the response content will be
            immediately downloaded.
        :param cert: (optional) if String, path to ssl client cert file
            (.pem). If Tuple, ('cert', 'key') pair.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        auth = AWSV4Sign(self.creds, self.region, self.service)
        session = requests.sessions.Session()
        req = requests.Request(
            method,
            url,
            data=data,
            headers=headers,
            params=params,
            cookies=cookies,
            files=files,
            auth=auth,
            json=json,
            hooks=hooks)
        prepped = req.prepare()
        response = session.send(prepped,
                                stream=stream,
                                verify=verify,
                                proxies=proxies,
                                cert=cert,
                                timeout=timeout,
                                allow_redirects=allow_redirects
                                )
        session.close()
        return response

    def get(self, url, params=None, **kwargs):
        """Sends a GET request.
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary or bytes to be sent in
            the query string for the :class:`Request`.
        :param **kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        kwargs.setdefault('allow_redirects', True)
        return self.request('get', url, params=params, **kwargs)

    def options(self, url, **kwargs):
        """Sends a OPTIONS request.
        :param url: URL for the new :class:`Request` object.
        :param **kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        kwargs.setdefault('allow_redirects', True)
        return self.request('options', url, **kwargs)

    def head(self, url, **kwargs):
        """Sends a HEAD request.
        :param url: URL for the new :class:`Request` object.
        :param **kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        kwargs.setdefault('allow_redirects', False)
        return self.request('head', url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        """Sends a POST request.
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, bytes, or file-like object
            to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of
            the :class:`Request`.
        :param **kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return self.request('post', url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        """Sends a PUT request.
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, bytes, or file-like object to
            send in the body of the :class:`Request`.
        :param **kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return self.request('put', url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        """Sends a PATCH request.
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, bytes, or file-like object to
            send in the body of the :class:`Request`.
        :param **kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return self.request('patch', url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        """Sends a DELETE request.
        :param url: URL for the new :class:`Request` object.
        :param **kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return self.request('delete', url, **kwargs)
