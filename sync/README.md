# Nextcloudcmd for Kubernetes

Runs [nextcloudcmd](https://docs.nextcloud.com/desktop/2.6/advancedusage.html#nextcloud-command-line-client)
in a loop in Docker. 

The synchronized directory is to be shared with Jupyter's single-user container 
(via K8S volumes) as the user home directory. 
This setup is created for instance by [our JupyterHub extension](../authorization/login-flow-v2). 

## Configure

The image is configured with the following environment variables:

* NC_URL - an URL (with `https://` and the trailing slash) of a Nextcloud instance
* NC_REMOTE_DIR - user directory in Nextcloud to be synchronized
* NC_USER - Nextcloud username
* NC_PASS - Nextcloud password, might be app password
* NC_LOCAL_DIR - local directory to be synchronized (optional, default: `/home/jovyan`)
* NC_INTERVAL - delay in seconds between subsequent runs (optional, default: 10)

## Build

```
docker build -t nc-sync .
```

## Run

```
docker run \
    --name nc-sync \
    -e NC_URL="https://drive.example.com/" \
    -e NC_REMOTE_DIR="notebooks" \
    -e NC_USER="username" \
    -e NC_PASS="secretpassword" \
    nc-sync
```
