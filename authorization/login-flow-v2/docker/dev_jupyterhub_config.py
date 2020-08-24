# This is for dev purposes only!
# It is not included in the official image.
c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'
c.JupyterHub.template_paths = ['/opt/templates']
c.JupyterHub.spawner_class = 'nextcloud_spawner.NextcloudLocalProcessSpawner'
