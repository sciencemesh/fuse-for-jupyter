from setuptools import setup


setup(
    name='nextcloud-spawner',
    version='0.0.1',
    description='JupyterHub Spawner with Nextcloud integration',
    packages=['nextcloud_spawner'],
    python_requires='>=3.5, <4',
    install_requires=[
        'requests',
        'cached_property',
        'jupyterhub',
    ],
)
