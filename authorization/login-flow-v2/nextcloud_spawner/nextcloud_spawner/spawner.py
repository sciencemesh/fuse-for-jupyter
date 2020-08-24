import os

from cached_property import cached_property
from jupyterhub.spawner import SimpleLocalProcessSpawner
from kubespawner import KubeSpawner

from .credentials import NcCredentials, NcCredentialsManager

# just checking if it's set because it's needed
os.environ['JUPYTERHUB_CRYPT_KEY']
NC_HANDLER_IMAGE = os.environ['NC_HANDLER_IMAGE']
NC_URL = os.environ['NC_URL']
NC_REMOTE_DIR = os.environ['NC_REMOTE_DIR']


class NextcloudSpawnerMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nc_handler_image = NC_HANDLER_IMAGE
        self.nc_url = NC_URL
        self.nc_remote_dir = NC_REMOTE_DIR

    def options_form(self, _):
        """ returns a HTML form if NC grant is needed """
        authz_url = self.get_authorization_url_if_needed()
        if authz_url:
            return authz_url
        else:
            return None

    def options_from_form(self, _):
        """ Validates the form
        i.e. raises error if NC grant is not completed
        or returns NC credentials to be stored in db (encrypted!), once it's completed
        """
        encrypted_nc_credentials = self.get_credentials_from_nc()
        if encrypted_nc_credentials:
            # returned data will be saved in the Hub db
            return encrypted_nc_credentials
        else:
            raise Exception('The access is not yet granted in Nextcloud!')

    def pre_spawn_hook(self, _):
        if not hasattr(self, 'extra_containers'):
            self.log.error('The spawner is %s, and it has no extra_containers field. ' +
                           'Not in K8S? Nextcloudcmd WILL NOT be run!', self)
            return

        try:
            nc_sync_container = {
                'name': 'nc-handler',
                'image': self.nc_handler_image,
                'volumeMounts': [{
                    'mountPath': '/home/jovyan',
                    'name': 'volume-{username}',
                }],
                'env': self.get_k8s_env(),
            }
            self.extra_containers.append(nc_sync_container)
        except NcCredentials.Invalid:
            # illegal state
            self.log.error('NC credentials cannot be read from user_options. The options are: %s' % self.user_options)
            raise Exception('Nextcloud credentials cannot be found. ' +
                            'If the problem persists, please contact administrator.')

    def get_authorization_url_if_needed(self):
        if self.has_valid_nc_credentials():
            self.log.info('NC credentials already stored in the database')
            return None
        else:
            self.log.info('getting NC authorization URL...')
            authz_url = self.nc_credentials_manager.get_authorization_url()
            self.log.info('NC authorization URL: %s' % authz_url)
            return authz_url

    def has_valid_nc_credentials(self):
        options = self._get_stored_user_options()
        try:
            nc_credentials = NcCredentials.from_encrypted_dict(options)
            return self.nc_credentials_manager.check_credentials_are_valid(nc_credentials)
        except NcCredentials.Invalid:
            return False

    def get_credentials_from_nc(self):
        try:
            self.log.info('trying to read credentials from NC...')
            nc_credentials = self.nc_credentials_manager.read_credentials()
            self.log.info('NC credentials successfully obtained!')
            return nc_credentials.to_encrypted_dict()
        except self.nc_credentials_manager.CredentialsNotAvailable:
            self.log.warning('NC credentials not available in NC!')
            return None

    @cached_property
    def nc_credentials_manager(self):
        return NcCredentialsManager(
            nc_url=self.nc_url,
            logger=self.log.info
        )

    def _get_stored_user_options(self):
        return self.orm_spawner.user_options or {}

    def get_k8s_env(self):
        env_list = list()
        for name, value in self.get_raw_env().items():
            env_list.append({
                'name': name,
                'value': value,
            })
        return env_list

    def get_raw_env(self):
        nc_credentials = NcCredentials.from_encrypted_dict(self._get_stored_user_options())
        env = dict()
        env['NC_URL'] = self.nc_url
        env['NC_REMOTE_DIR'] = self.nc_remote_dir
        env['NC_USER'] = nc_credentials.user
        env['NC_PASS'] = nc_credentials.password
        return env


class NextcloudLocalProcessSpawner(NextcloudSpawnerMixin, SimpleLocalProcessSpawner):
    pass


class NextcloudKubeSpawner(NextcloudSpawnerMixin, KubeSpawner):
    pass
