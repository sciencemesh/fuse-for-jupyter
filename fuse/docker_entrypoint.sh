#!/bin/bash
set -eu

# prepare mount target
MOUNT_TARGET=$(realpath ~)/$WEBDAV_LOCAL_DIR
echo "WebDAV to be mounted in $MOUNT_TARGET"
mkdir -p $MOUNT_TARGET
echo "$WEBDAV_ENDPOINT $MOUNT_TARGET davfs user,rw,noauto 0 0" >> /etc/fstab

# configure WebDAV credentials
mkdir ~/.davfs2
chmod ug-s ~/.davfs2
echo "$MOUNT_TARGET $WEBDAV_USER $WEBDAV_PASS" >> ~/.davfs2/secrets
chmod 600 ~/.davfs2/secrets

# umount on exit to synchronize files
cleanup() {
    echo "Container stopped, unmounting WebDAV..."
    until umount $MOUNT_TARGET; do
        echo "Problem when unmounting. Retrying in 2 seconds..."
        sleep 2
    done
    echo "Done"
    exit 0
}
trap 'cleanup' SIGTERM SIGINT SIGHUP

# mount WebDAV
echo "Mounting WebDAV..."
mount $MOUNT_TARGET

# running CMD, usually the notebook server
"${@}"

# umount on exit to synchronize files
cleanup
