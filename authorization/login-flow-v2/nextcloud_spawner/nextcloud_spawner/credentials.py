import os

import requests
from requests.auth import HTTPBasicAuth
from traitlets.config import LoggingConfigurable

from .crypto import encrypt, decrypt

NC_JUPYTER_LABEL = os.environ['NC_JUPYTER_LABEL']


class NcCredentials:

    _DICT_NAME_USER = 'nc_user'
    _DICT_NAME_PASSWORD = 'nc_pass'

    class DeserializationError(Exception):
        pass

    @classmethod
    def from_encrypted_dict(cls, dict):
        try:
            user = decrypt(dict[cls._DICT_NAME_USER])
            password = decrypt(dict[cls._DICT_NAME_PASSWORD])
            return cls(user, password)
        except KeyError:
            raise cls.DeserializationError()

    def __init__(self, user, password):
        self.user = user
        self.password = password

    def __repr__(self):
        return 'user=%s, password=%s' % (self.user, self.password)

    def to_encrypted_dict(self):
        return {
            self._DICT_NAME_USER: encrypt(self.user),
            self._DICT_NAME_PASSWORD: encrypt(self.password),
        }


class NcAuthorizationFlow(LoggingConfigurable):
    """ Client to Nextcloud's Login Flow v2 (i.e. authorization flow)
    https://docs.nextcloud.com/server/latest/developer_manual/client_apis/LoginFlow/index.html#login-flow-v2
    """

    # client name that is to be presented in Nextcloud
    client_name = NC_JUPYTER_LABEL

    class CredentialsNotYetAvailable(Exception):
        pass

    def __init__(self, nc_url):
        self.nc_url = nc_url if not nc_url.endswith('/') else nc_url[:-1]
        self._authorization_url = None
        self._poll_endpoint = None
        self._poll_endpoint_token = None

    def get_authorization_url(self):
        if not self._authorization_url:
            self.log.info('generating new NC authorization URL...')
            self._initiate_authorization_flow()
            self.log.info('NC authorization URL: %s' % self._authorization_url)
        return self._authorization_url

    def _initiate_authorization_flow(self):
        r = self._request('POST', '/login/v2')
        r.raise_for_status()
        obj = r.json()
        self._authorization_url = obj['login']
        self._poll_endpoint = obj['poll']['endpoint']
        self._poll_endpoint_token = obj['poll']['token']

    def read_credentials(self):
        if not self._poll_endpoint:
            raise ValueError('Illegal state: poll endpoint is unknown, authorization flow not initialized')
        r = self._request('POST', self._poll_endpoint, data={'token': self._poll_endpoint_token})
        if r.status_code == 404:
            raise self.CredentialsNotYetAvailable()
        r.raise_for_status()
        obj = r.json()
        return NcCredentials(obj['loginName'], obj['appPassword'])

    def check_credentials_are_valid(self, nc_credentials):
        r = self._request('GET', '/apps/files', auth=HTTPBasicAuth(nc_credentials.user, nc_credentials.password))
        return r.status_code == 200

    def _request(self, method, path, **kwargs):
        if path.startswith('https://') or path.startswith('http://'):
            url = path
        else:
            url = self._build_url(path)
        self.log.info('%s %s' % (method, url))
        r = requests.request(method, url, headers={
            'User-Agent': self.client_name,
        }, **kwargs)
        return r

    def _build_url(self, path):
        assert not self.nc_url.endswith('/'), self.nc_url
        assert path.startswith('/'), path
        return self.nc_url + path
