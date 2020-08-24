# Example for Z2JH

The sync and login-flow-v2 approaches implemented within 
[Zero To JupyterHub](https://zero-to-jupyterhub.readthedocs.io/) (Z2JH).

Tested with [Z2JH charts](https://github.com/jupyterhub/helm-chart) 
v. 0.9.0.

## Setup

First, build our Docker images and push them somewhere, 
so your Kubernetes cluster can access them:

- the [JupyterHub image](../../authorization/login-flow-v2/docker)
- the [nc-sync image](../../sync)

Assume the images are pushed to DockerHub as, respectively:

```
example/jupyterhub:latest
example/nc-sync:latest
```

Setup JupyterHub as [documented in Z2JH](https://zero-to-jupyterhub.readthedocs.io/en/latest/setup-jupyterhub/setup-jupyterhub.html),
adjusting `config.yaml` as follows:

```
hub:
  image:
    name: example/jupyterhub
    tag: latest
  templatePaths:
    # the custom templates added in the JupyterHub image
    - /opt/templates
  extraConfig: |-
    config = '/etc/jupyter/jupyter_notebook_config.py'
    c.Spawner.cmd = ['jupyter-labhub']
    c.JupyterHub.spawner_class = 'nextcloud_spawner.NextcloudKubeSpawner'
  extraEnv:
    JUPYTERHUB_CRYPT_KEY: sUpeRSecReT12345
    NC_HANDLER_IMAGE: example/nc-sync:latest 
    NC_URL: https://drive.example.com/
    NC_REMOTE_DIR: notebooks
    NC_JUPYTER_LABEL: Jupyter Test instance
```
