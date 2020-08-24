# Nextcloud-authorization extension for Z2JH

Implementation of this Nextcloud-authorization extension within
a JupyterHub image from
[Zero To JupyterHub](https://zero-to-jupyterhub.readthedocs.io/).

## Build

[Dockerfile](Dockerfile) defines two version of the image (i.e. a multi-stage build):

- jupyterhub-official - the main, 'official', image
- jupyterhub-dev - the extended image for local development

The version (the build stage) is specified in `docker build` as given below.

Run in the current directory:

```
docker build .. \
    -f Dockerfile \
    --target jupyterhub-dev \
    -t jupyterhub-dev
``` 

## Run locally

```
docker run \
    --name jupyterhub \
    -p 8000:8000 \
    -e NC_HANDLER_IMAGE="" \
    -e NC_URL="https://drive.example.com/" \
    -e NC_REMOTE_DIR="notebooks" \
    -e NC_JUPYTER_LABEL="Jupyter Dev Instance" \
    -e JUPYTERHUB_CRYPT_KEY=$(openssl rand -hex 32) \
    jupyterhub-dev
```
