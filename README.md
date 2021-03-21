# HowTo lakeFS

## Prerequistes
1. Install ``docker`` & ``docker-compose``
2. Install ``poetry`` and setup the venv using ``poetry install``

## Run lakeFS locally
1. Run ``docker-compose up -d`` inside of the ``docker`` directory. This starts two containers, the lakeFS Web UI and a postgres metadatabase. 
The web UI should be running under ``localhost:8000``, so make sure this port is not already occupied.
2. To initialize the service, a first user must be created. Make sure to store the credentials somewhere safe.
3. Now you can create a repository, additional users and upload and commit files via the web UI or the CLI, ``lakectl``.
When creating a repository, you must specify a storage location. This could be a remote storage or a local directory, for example ``local://Users/<user>/<local>/<path>``. This is also called the storage namespace.

## lakeFS CLI
To access the CLI run ``docker exec -it <lakefs_ui_container> sh``. Creating a repository via the CLI requires the URI to be speciefied for example:
``lakectl repo create lakefs://my-repo local://Users/<user>/<local>/<path>``. The URI must also be used when committing data, creating new branches or merging existing branches.

