# https://github.com/jupyterhub/zero-to-jupyterhub-k8s/tree/master/images/singleuser-sample
FROM jupyterhub/k8s-singleuser-sample:0.9.0

USER root
RUN apt-get update && \
    apt-get install -y davfs2 && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

RUN chmod +s /sbin/mount.davfs && \
    chown $NB_USER: /etc/fstab && \
    usermod -aG davfs2 $NB_USER

COPY davfs2.conf /etc/davfs2/davfs2.conf

COPY docker_entrypoint.sh /docker_entrypoint.sh

ENTRYPOINT ["tini", "-g", "--", "/docker_entrypoint.sh"]
CMD ["start-notebook.sh"]

USER $NB_USER

