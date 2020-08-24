FROM alpine:3.12.0

# Install nextcloudcmd and other dependencies
RUN apk update && \
    apk add --no-cache \
        nextcloud-client \
        curl && \
    rm -rf /etc/apk/cache

# Assert that it works properly.
# It is not necessary but there were weird dependency issues depending on build environment,
# so let's leave it here as an assertion.
RUN nextcloudcmd --version

# Create a non-root user
# For simplicity, the user is the same as in Jupyter containers.
ENV NB_USER=jovyan \
    NB_UID=1000 \
    NB_GID=100 \
    HOME=/home/jovyan
RUN adduser -D -g $NB_GID -u $NB_UID -h $HOME $NB_USER
WORKDIR $HOME

# Default config for nc-sync
ENV NC_LOCAL_DIR=$HOME \
    NC_INTERVAL=10

COPY nc-sync /usr/bin/nc-sync
RUN chmod +x /usr/bin/nc-sync
CMD ["nc-sync", "--loop"]

USER $NB_USER
