# FUSE mount via webDAV

This Docker image makes a FUSE mount, in Jupyter, of EFSS files accessed via webDAV.

This Docker image is a Jupyter's single-user image.
The base image comes from [Zero to JupyterHub](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/tree/master/images/singleuser-sample). 

## Configure

The image is configured with the following environment variables:

* WEBDAV_ENDPOINT - WebDAV endpoint, pointing at a remote directory 
* WEBDAV_USER - username
* WEBDAV_PASS - password
* WEBDAV_LOCAL_DIR - local directory, within the user's home directory, 
to mount the remote files 

See examples below. 

## Build

```
docker build -t davfs .
```

## Run

It requires to be run as privileged container or with `SYS_ADMIN` capability.
It also requires the access to `/dev/fuse` on the Docker host.

For instance:

```
docker run \
    --cap-add SYS_ADMIN \
    --device /dev/fuse \
    -p 8888:8888 \
    -e JUPYTER_ENABLE_LAB=true \
    -e WEBDAV_ENDPOINT=https://drive.example.com/remote.php/dav/files/user/ \
    -e WEBDAV_USER=user \
    -e WEBDAV_PASS=secret123 \
    -e WEBDAV_LOCAL_DIR=drive \
    davfs
```

Notes:
* The home directory is `/home/jovyan`, so the remote files will be mounted to `/home/jovyan/drive`.
* `JUPYTER_ENABLE_LAB` is the base image's config option to enable the JupyterLab user interface.
