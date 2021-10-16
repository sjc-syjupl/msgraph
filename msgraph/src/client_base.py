import requests
from . import exceptions
from urllib.parse import urlencode


class Client_Base(object):
    AUTHORITY_URL = 'https://login.microsoftonline.com/'
    AUTH_ENDPOINT = '/oauth2/v2.0/authorize?'
    TOKEN_ENDPOINT = '/oauth2/v2.0/token'
    RESOURCE = 'https://graph.microsoft.com/'
    SCOPE = 'https://graph.microsoft.com/.default'

    OFFICE365_AUTHORITY_URL = 'https://login.live.com'
    OFFICE365_AUTH_ENDPOINT = '/oauth20_authorize.srf?'
    OFFICE365_TOKEN_ENDPOINT = '/oauth20_token.srf'

    def __init__(self, client_id=None, client_secret=None, account_id=None, tenant=None, api_version='v1.0', account_type='common', office365=False, config=None):
        self.tenant = tenant
        self.account_id = account_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_version = api_version
        self.account_type = account_type

        self.username = None
        self.password = None
        self.redirect_uri = None

        self.token = None
        self.office365 = office365
        self.office365_token = None
        self.init(config)

    def init(self, config):
        if config:
            if 'tenant' in config:
                self.tenant = config['tenant']
            if 'account_id' in config:
                self.account_id = config['account_id']
            if 'client_id' in config:
                self.client_id = config['client_id']
            if 'client_secret' in config:
                self.client_secret = config['client_secret']
            if 'api_version' in config:
                self.api_version = config['api_version']
            if 'account_type' in config:
                self.account_type = config['account_type']

            if 'username' in config:
                self.username = config['username']
            if 'password' in config:
                self.password = config['password']
            if 'redirect_uri' in config:
                self.redirect_uri = config['redirect_uri']

            if 'token' in config:
                self.token = config['token']
            if 'office365' in config:
                self.office365 = config['office365']
            if 'office365_token' in config:
                self.office365_token = config['office365_token']
        self.base_url = self.RESOURCE + self.api_version + '/'
        if self.account_id:
            self.set_account(self.account_id)
        else:
            self.set_me()

    def set_me(self):
        self.context = 'me/'

    def set_account(self, account_id):
        self.account_id = account_id
        self.context = 'users/{}/'.format(account_id)

    #
    #  auth
    #
    def auth_by_secret_id(self):
        if not self.client_id:
            raise exceptions.ClientRequired('You must set the Client_Id.')
        if not self.client_secret:
            raise exceptions.SecretRequired('You must set the Secret_Id.')
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': self.SCOPE,
            'grant_type': 'client_credentials',
        }
        response = requests.post(
            self.AUTHORITY_URL + self.tenant + self.TOKEN_ENDPOINT, data=data)
        self.set_token(self._parse(response))
        if self.username and not self.account_id:
            self.set_account(self.username)
        return self.token

    def auth_by_password(self, scope, username=None, password=None):
        data = {
            'client_id': self.client_id,
            'scope':  scope if isinstance(scope, str) else ' '.join(scope),
            'grant_type': 'password',
            'username': username if username else self.username,
            'password': password if password else self.password,
        }
        if self.client_secret:
            data['client_secret'] = self.client_secret
        print(self.AUTHORITY_URL + self.tenant + self.TOKEN_ENDPOINT)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(
            self.AUTHORITY_URL + self.tenant + self.TOKEN_ENDPOINT, data=data, headers=headers)
        self.set_token(self._parse(response))
        return self.token

    def auth_by_redirect_uri(self, scope, redirect_uri=None, state=None):
        params = {
            'client_id': self.client_id,
            'redirect_uri': redirect_uri if redirect_uri else self.redirect_uri,
            'scope': ' '.join(scope),
            'response_type': 'code',
            'response_mode': 'query'
        }

        if state:
            params['state'] = state
        if self.office365:
            response = self.OFFICE365_AUTHORITY_URL + \
                self.OFFICE365_AUTH_ENDPOINT + urlencode(params)
        else:
            response = self.AUTHORITY_URL + self.account_type + \
                self.AUTH_ENDPOINT + urlencode(params)
        return response

    def exchange_code(self, code, redirect_uri=None):
        data = {
            'client_id': self.client_id,
            'redirect_uri': redirect_uri if redirect_uri else self.redirect_uri,
            'code': code,
            'grant_type': 'authorization_code',
        }
        if self.client_secret:
            data['client_secret'] = self.client_secret
        if self.office365:
            response = requests.post(
                self.OFFICE365_AUTHORITY_URL + self.OFFICE365_TOKEN_ENDPOINT, data=data)
        else:
            response = requests.post(
                self.AUTHORITY_URL + self.account_type + self.TOKEN_ENDPOINT, data=data)
        return self._parse(response)

    def refresh_token(self, refresh_token, redirect_uri=None):
        data = {
            'client_id': self.client_id,
            'redirect_uri': redirect_uri if redirect_uri else self.redirect_uri,
            'client_secret': self.client_secret,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token',
        }
        if self.office365:
            response = requests.post(
                self.OFFICE365_AUTHORITY_URL + self.OFFICE365_TOKEN_ENDPOINT, data=data)
        else:
            response = requests.post(
                self.AUTHORITY_URL + self.account_type + self.TOKEN_ENDPOINT, data=data)
        return self._parse(response)

    def set_token(self, token):
        """Sets the Token for its use in this library.

        Args:
            token: A string with the Token.

        """
        if self.office365:
            self.office365_token = token
        else:
            self.token = token

    #
    #  Generic function
    #
    def get(self, argument, params=None, token_required=True):
        """Generic get

        Args:
            argument: API access point to be pasted to base_url
            params: A dict.

        Returns:
            A dict.

        """
        if token_required and not self.token:
            raise exceptions.TokenRequired('You must set the Token.')
        return self._get(self.base_url + argument, params=params)

    def post(self, argument, params=None, token_required=True):
        if token_required and not self.token:
            raise exceptions.TokenRequired('You must set the Token.')
        return self._post(self.base_url + argument, params=params)

    def put(self, argument, params=None, token_required=True):
        if token_required and not self.token:
            raise exceptions.TokenRequired('You must set the Token.')
        return self._post(self.base_url + argument, params=params)

    def patch(self, argument, params=None, token_required=True):
        if token_required and not self.token:
            raise exceptions.TokenRequired('You must set the Token.')
        return self._patch(self.base_url + argument, params=params)

    def delete(self, argument, params=None, token_required=True):
        if token_required and not self.token:
            raise exceptions.TokenRequired('You must set the Token.')
        return self._delete(self.base_url + argument, params=params)

    #
    #
    #

    def _get(self, url, **kwargs):
        return self._request('GET', url, **kwargs)

    def _post(self, url, **kwargs):
        return self._request('POST', url, **kwargs)

    def _put(self, url, **kwargs):
        return self._request('PUT', url, **kwargs)

    def _patch(self, url, **kwargs):
        return self._request('PATCH', url, **kwargs)

    def _delete(self, url, **kwargs):
        return self._request('DELETE', url, **kwargs)

    def _request(self, method, url, headers=None, **kwargs):
        _headers = {
            'Accept': 'application/json',
        }
        try:
            if self.office365:
                _headers['Authorization'] = 'Bearer ' + \
                    self.office365_token['access_token']
            else:
                _headers['Authorization'] = 'Bearer ' + \
                    self.token['access_token']
        except TypeError:
            if self.office365:
                _headers['Authorization'] = 'Bearer ' + self.office365_token
            else:
                _headers['Authorization'] = 'Bearer ' + self.token
        if headers:
            _headers.update(headers)
        if 'files' not in kwargs:
            # If you use the 'files' keyword, the library will set the Content-Type to multipart/form-data
            # and will generate a boundary.
            _headers['Content-Type'] = 'application/json'
        print("METHOD: "+method)
        print("URL: "+url)
        print("HEADERS: "+str(_headers))
        print("ARG: "+str(kwargs))
        return self._parse(requests.request(method, url, headers=_headers, **kwargs))

    def _parse(self, response):
        status_code = response.status_code
        if 'application/json' in response.headers.get('Content-Type', ''):
            r = response.json()
        else:
            r = response.content
        if status_code in (200, 201, 202, 206):
            return r
        elif status_code == 302:  # redirect
            return response.headers['Location']
        elif status_code == 204:
            return None
        elif status_code == 400:
            raise exceptions.BadRequest(r)
        elif status_code == 401:
            raise exceptions.Unauthorized(r)
        elif status_code == 403:
            raise exceptions.Forbidden(r)
        elif status_code == 404:
            raise exceptions.NotFound(r)
        elif status_code == 405:
            raise exceptions.MethodNotAllowed(r)
        elif status_code == 406:
            raise exceptions.NotAcceptable(r)
        elif status_code == 409:
            raise exceptions.Conflict(r)
        elif status_code == 410:
            raise exceptions.Gone(r)
        elif status_code == 411:
            raise exceptions.LengthRequired(r)
        elif status_code == 412:
            raise exceptions.PreconditionFailed(r)
        elif status_code == 413:
            raise exceptions.RequestEntityTooLarge(r)
        elif status_code == 415:
            raise exceptions.UnsupportedMediaType(r)
        elif status_code == 416:
            raise exceptions.RequestedRangeNotSatisfiable(r)
        elif status_code == 422:
            raise exceptions.UnprocessableEntity(r)
        elif status_code == 429:
            raise exceptions.TooManyRequests(r)
        elif status_code == 500:
            raise exceptions.InternalServerError(r)
        elif status_code == 501:
            raise exceptions.NotImplemented(r)
        elif status_code == 503:
            raise exceptions.ServiceUnavailable(r)
        elif status_code == 504:
            raise exceptions.GatewayTimeout(r)
        elif status_code == 507:
            raise exceptions.InsufficientStorage(r)
        elif status_code == 509:
            raise exceptions.BandwidthLimitExceeded(r)
        else:
            if r['error']['innerError']['code'] == 'lockMismatch':
                # File is currently locked due to being open in the web browser
                # while attempting to reupload a new version to the drive.
                # Thus temporarily unavailable.
                raise exceptions.ServiceUnavailable(r)
            raise exceptions.UnknownError(r)
