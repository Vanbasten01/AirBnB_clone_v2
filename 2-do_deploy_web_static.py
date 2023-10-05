#!/usr/bin/python3
# a Fabric script (based on the file 1-pack_web_static.py)
# that distributes an archive to your web servers,
# using the function do_deploy.

from os.path import exists, isfile
from datetime import datetime
from fabric.api import local, run, put, env

env.hosts = ['18.206.207.65', '54.90.18.138']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """Create a compressed archive of the web_static folder.
    Returns:
        str: The name of the created archive file,
        or None if the operation fails.
    """
    try:
        now = datetime.now()
        local("mkdir -p versions")
        archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
                now.year, now.month, now.day, now.hour,
                now.minute, now.second)
        local("tar -czvf versions/{} web_static".format(archive_name))
        return archive_name
    except Exception:
        return None


def do_deploy(archive_path):
    """Distribute an archive to web servers.
    Args:
        archive_path (str): The path to the archive file to be deployed.
    Returns:
        bool: True if the deployment succeeds, False otherwise.
    """
    if not exists(archive_path) and not isfile(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        filename = archive_path.split('/')[-1].split('.')[0]
        release_path = "/data/web_static/releases/{}/".format(filename)
        run("mkdir -p {}".format(release_path))
        run("sudo tar -xzf /tmp/{}.tgz -C {}".format(filename, release_path))

        # delete the archive from the server
        run("sudo rm /tmp/{}.tgz".format(filename))
        # remove the symbolic link from the server
        run("rm -rf /data/web_static/current")
        run("mv {}/web_static/* {}".format(release_path, release_path))
        run("rm -rf {}/web_static/".format(release_path))

        # create a new symbolic link
        run("sudo ln -sf {} /data/web_static/current".format(release_path))
        return True
    except Exception:
        return False
